from fastapi import Depends, APIRouter, HTTPException, status
from .. databases import get_db
from ..import schemas, models, oauth2
from sqlalchemy.orm import Session

router=APIRouter(
    tags=['Vote']
)

@router.post("/vote",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    valid_post= db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if valid_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not a valid post")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    found=vote_query.first()
    if vote.dir ==1:
        if found :
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail=f"user {current_user.id} has already voted on {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"msg":"voted sucessfully"}
    else:
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not voted before")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"msg":"sucessfully deleted vote"}

        