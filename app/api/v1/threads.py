from sqlalchemy import func
from app import models, schemas
from app.api.deps import db_dependency
from fastapi import status, HTTPException, APIRouter, Depends
from typing import List, Optional
from app.core import security

router = APIRouter(prefix="/threads", tags=["Threads"])


@router.get("/all", response_model=List[schemas.ThreadResponse])
def get_all_threads(
    db: db_dependency,
    current_user: models.User = Depends(security.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    threads = (
        db.query(models.Thread, func.count(models.Vote.thread_id).label("votes"))
        .join(models.Vote, models.Vote.thread_id == models.Thread.id, isouter=True)
        .group_by(models.Thread.id)
        .filter(models.Thread.content.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return threads


@router.get("/", response_model=List[schemas.ThreadResponse])
def get_all_threads(
    db: db_dependency, current_user: models.User = Depends(security.get_current_user)
):
    threads = (
        db.query(models.Thread).filter(models.Thread.owner_id == current_user.id).all()
    )
    return threads


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ThreadResponse
)
def create_thread(
    thread: schemas.ThreadCreate,
    db: db_dependency,
    current_user: models.User = Depends(security.get_current_user),
):
    new_thread = models.Thread(owner_id=current_user.id, **thread.model_dump())
    db.add(new_thread)
    db.commit()
    db.refresh(new_thread)
    return new_thread


@router.get("/{id}")
def get_thread(id: int, db: db_dependency):
    extracted_thread = (
        db.query(models.Thread, func.count(models.Vote.thread_id).label("votes"))
        .join(models.Vote, models.Vote.thread_id == models.Thread.id, isouter=True)
        .group_by(models.Thread.id)
        .filter(models.Thread.id == id)
        .first()
    )
    if not extracted_thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"thread with id: {id} not found",
        )
    return extracted_thread


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_thread(
    id: int,
    db: db_dependency,
    current_user: models.User = Depends(security.get_current_user),
):
    potential_found_thread_query = db.query(models.Thread).filter(
        models.Thread.id == id
    )
    potential_found_thread = (
        db.query(models.Thread).filter(models.Thread.id == id).first()
    )
    if potential_found_thread is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thread with id: {id} doesn't exist",
        )
    if potential_found_thread.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform that action",
        )
    potential_found_thread_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Thread deleted successfully"}


@router.put("/{id}")
def update_thread(
    id: int,
    thread: schemas.ThreadUpdate,
    db: db_dependency,
    current_user: models.User = Depends(security.get_current_user),
):
    thread_query = db.query(models.Thread).filter(models.Thread.id == id)
    extracted_thread = thread_query.first()
    if extracted_thread == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"thread with id: {id} doesn't exist",
        )
    if extracted_thread.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform that action",
        )
    thread_query.update(thread.model_dump(), synchronize_session=False)
    db.commit()
    return thread_query.first()
