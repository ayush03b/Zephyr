from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas
from app.api.deps import db_dependency
from app.core import security

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post('/token', response_model=schemas.Token)
def create_token(db: db_dependency, user_credentials: OAuth2PasswordRequestForm = Depends()):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not security.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = security.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}