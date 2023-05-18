from fastapi import APIRouter
from api.app.api_v1.endpoints import index, questions

api_router = APIRouter()
api_router.include_router(index.router, tags=["index"])
api_router.include_router(questions.router, tags=["question"])
