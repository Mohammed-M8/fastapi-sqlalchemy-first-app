from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.get_current_user import get_current_user
from models.comment import CommentModel
from models.tea import TeaModel
from models.user import UserModel
from serializers.comment import CommentSchema, CreateCommentSchema, UpdateCommentSchema
from typing import List
from database import get_db

router = APIRouter()

@router.get('/teas/{tea_id}/comments',response_model=List[CommentSchema])
def get_comments(tea_id:int,db:Session=Depends(get_db)):
    comments=db.query(CommentModel).filter(CommentModel.tea_id==tea_id).all()
    return comments

@router.get('/comments/{comment_id}',response_model=CommentSchema)
def get_single_comment(comment_id:int,db:Session=Depends(get_db)):
    comment=db.query(CommentModel).filter(CommentModel.id==comment_id).first()
    if not comment:
        raise HTTPException(404,"comment not found")
    return comment

@router.post('/teas/{tea_id}/comments',response_model=CommentSchema,status_code=201)
def create_comment(tea_id:int,new_comment:CreateCommentSchema,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    new_data=CommentModel(**new_comment.model_dump(),tea_id=tea_id,user_id=current_user.id)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.put('/comments/{comment_id}',status_code=204)
def update_comment(comment_id:int,comment:UpdateCommentSchema,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    old_comment=db.query(CommentModel).filter(CommentModel.id==comment_id).first()
    if not old_comment:
        raise HTTPException(404,"comment not found")

    if old_comment.user_id!=current_user.id:#type:ignore
        raise HTTPException(403,"Forbidden")
    
    comment_data=comment.model_dump(exclude_unset=True)
    for key,value in comment_data.items():
        setattr(old_comment,key,value)

    db.commit()
    db.refresh(old_comment)
    return old_comment

@router.delete('/comments/{comment_id}',status_code=204)
def delete_comment(comment_id:int,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    comment_to_delete=db.query(CommentModel).filter(CommentModel.id==comment_id).first()
    if not comment_to_delete:
        raise HTTPException(404,"comment not found")

    if comment_to_delete.user_id!=current_user.id:#type:ignore
        raise HTTPException(403,"Forbidden")
    
    db.delete(comment_to_delete)
    db.commit()
    return None