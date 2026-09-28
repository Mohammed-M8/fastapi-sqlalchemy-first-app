from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel


from .comment import CommentModel


class TeaModel(BaseModel):
    __tablename__="teas"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True)
    in_stock=Column(Boolean)
    rating=Column(Integer)
    comments=relationship('CommentModel',back_populates='tea')