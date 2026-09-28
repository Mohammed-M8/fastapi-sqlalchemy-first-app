
from datetime import datetime, timedelta, timezone
from warnings import deprecated

import jwt
from sqlalchemy import Column, Integer, String
from .base import BaseModel
from passlib.context import CryptContext
from config.environment import secret
from sqlalchemy.orm import relationship

pwd_context=CryptContext(["bcrypt"],deprecated="auto")

class UserModel(BaseModel):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)  # Each username must be unique
    email = Column(String, unique=True)  # Each email must be unique
    password=Column(String,nullable=True)

    teas=relationship('TeaModel',back_populates='user')

    def set_password(self,password:str):
        self.password=pwd_context.hash(password)

    def verify_password(self,password:str)->bool:
        return pwd_context.verify(password,self.password)

    def generate_token(self,**kwargs):
        payload={
            "exp":datetime.now(timezone.utc)+timedelta(days=1),
            "iat":datetime.now(timezone.utc),
            "sub":str(self.id),
        }
        

        token=jwt.encode(payload,secret,algorithm="HS256")

        return token