from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from data import tea_data
from models import tea
from models.tea import TeaModel
from serializers.tea import CreateTeaSchema, TeaSchema, UpdateTeaSchema
from typing import List
from database import get_db

router = APIRouter()

@router.get('/teas',response_model=List[TeaSchema])
def get_teas(db:Session=Depends(get_db)):
    teas=db.query(TeaModel).all()
    return teas

@router.get("/teas/{tea_id}",response_model=TeaSchema)
def get_single_tea(tea_id: int,db:Session=Depends(get_db)):
  tea=db.query(TeaModel).filter(TeaModel.id==tea_id).first()
  if not tea:
       raise HTTPException(status_code=404, detail="Cannot find Tea")
  return tea


@router.post("/teas",response_model=TeaSchema,status_code=201)
def create_tea(tea: CreateTeaSchema,db:Session=Depends(get_db)):
    new_data=TeaModel(**tea.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.put("/teas/{tea_id}")
def update_tea(tea_id: int, tea: UpdateTeaSchema,db:Session=Depends(get_db)):
    oldTea=db.query(TeaModel).filter(TeaModel.id==tea_id).first()
    if not oldTea:
        raise HTTPException(404,"Tea not found")

    tea_data=tea.model_dump(exclude_unset=True)
    for key,value in tea_data.items():
        setattr(oldTea,key,value)
    db.commit()
    db.refresh(oldTea)
    return oldTea
    




@router.delete("/teas/{tea_id}",status_code=204)
def delete_tea(tea_id: int,db:Session=Depends(get_db)):
    tea_to_delete=db.query(TeaModel).filter(TeaModel.id==tea_id).first()
    if not tea_to_delete:
            raise HTTPException(status_code=404, detail="Tea not found")
    db.delete(tea_to_delete)
    db.commit()
    return None