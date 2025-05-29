from fastapi import FastAPI
from .db_setup import engine
from app import models
from app.api.v1 import api_router
from app.core.config import settings

models.Base.metadata.create_all(
    bind=engine
)  # this is what actually crates the tables in the db when u run the app

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"data": "API working!"}
