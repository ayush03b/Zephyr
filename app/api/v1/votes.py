from app import models, schemas
from app.api.deps import db_dependency
from fastapi import status, HTTPException, APIRouter, Depends
from typing import List, Optional
from app.core import security

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def get_all_threads(vote: schemas.Vote, db: db_dependency, current_user: models.User = Depends(security.get_current_user)):
    post = db.query(models.Thread).filter(models.Thread.id == vote.thread_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Thread with id {vote.thread_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.thread_id == vote.thread_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on thread{vote.thread_id}")
        new_vote = models.Vote(thread_id=vote.thread_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "sucessfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message" : "sucessfully deleted vote"}