from fastapi import Depends, Request, FastAPI
from app.models import Question as QuestionModel


async def get_app(request: Request) -> FastAPI:
    return request.app

app_dependency = Depends(get_app)