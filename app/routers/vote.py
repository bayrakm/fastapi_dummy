from fastapi import  status, HTTPException, Response, APIRouter, Depends
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    # if there is no post
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {vote.post_id}")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first() 

    if (vote.dir == 1):
        
        # if already voted 
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}

    # to delete a vote direction is 0
    else:
        # if there is no such vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_error=False)
        db.commit()

        return {"message":"Successfully deleted vote"}


        