from app import models, schemas
from app.api.deps import db_dependency
from fastapi import status, HTTPException, APIRouter, Depends
from typing import List
from app.core import security

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
)

@router.get("/", response_model=List[schemas.ThreadResponse])
def get_all_threads(db: db_dependency):
    threads = db.query(models.Thread).all()
    return threads

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ThreadResponse)
def create_thread(thread: schemas.ThreadCreate, db: db_dependency, current_user: int = Depends(security.get_current_user)):
    new_thread = models.Thread(**thread.model_dump())
    db.add(new_thread)
    db.commit()
    db.refresh(new_thread)
    return new_thread

@router.get("/{id}")
def get_thread(id: int, db: db_dependency):
    extracted_thread = db.query(models.Thread).filter(models.Thread.id == id).first()
    if not extracted_thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"thread with id: {id} not found")
    return extracted_thread

@router.delete("/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_thread(id: int, db: db_dependency, current_user: int = Depends(security.get_current_user)):
    potential_found_thread = db.query(models.Thread).filter(models.Thread.id == id)
    if potential_found_thread.filter() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"thread with id: {id} doesn't exist")
    potential_found_thread.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}")
def update_thread(id: int, thread: schemas.ThreadUpdate, db: db_dependency, current_user: int = Depends(security.get_current_user)):
    thread_query = db.query(models.Thread).filter(models.Thread.id == id)
    extracted_thread = thread_query.first()
    if extracted_thread == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"thread with id: {id} doesn't exist")
    thread_query.update(thread.model_dump(), synchronize_session=False)
    db.commit()
    return thread_query.first()