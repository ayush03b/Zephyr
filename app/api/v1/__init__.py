from fastapi import APIRouter
from . import threads, users, auth, votes

api_router = APIRouter()
api_router.include_router(threads.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(votes.router)