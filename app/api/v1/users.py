from app import models, schemas
from app.api.deps import db_dependency
from fastapi import status, HTTPException, APIRouter
from typing import List
from app.core import security

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: db_dependency):
    users = db.query(models.User).all()
    return users

@router.post("/",response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: db_dependency):
    hashed_password = security.get_password_hash(user.password)
    user.password = hashed_password

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with email : {user.email} already exists")

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found!")
    return user