from fastapi import Depends, APIRouter, HTTPException, status
from .. import schemas, models, oauth2
from ..databases import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func


router =APIRouter(
    tags=['users']
)

## using sqlalchemy

@router.get("/sqlalchemy",response_model=List[schemas.PostVote])
def root(db: Session = Depends(get_db),limit:int =10,skip:int =0,search:str=""):
 #   posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter =True).group_by(models.Post.id).all()
    return posts

@router.get("/sqlalchemy/{id}",response_model=schemas.PostVote)
def get( id:int, db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
    #new_post=db.query(models.Post).filter(models.Post.id == id).first()
    new_post= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter =True).group_by(models.Post.id).filter(models.Post.id == id).first()
    return new_post

@router.post("/sqlalchemy",response_model=schemas.DetailsResponse)
def post(post:schemas.Details, db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/sqlalchemy/{id}")
def delete(id:int, db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)
    if post.first() == None:
        return {"msg":f"{id} not found"}
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorised attempt")
    post.delete(synchronize_session=False)
    db.commit()
    return {"message":"deleted sucessfully"}

@router.put("/sqlalchemy/{id}")
def put(id:int,post:schemas.Details, db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        return {"msg":f"{id} not found"}
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorised attempt")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"msg":post_query.first()}

    