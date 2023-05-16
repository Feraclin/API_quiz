from typing import List, TYPE_CHECKING

import httpx as httpx
from fastapi import HTTPException, APIRouter, FastAPI
from sqlalchemy import select

from app.api_v1.deps import app_dependency
from app.schemas import Question, QuestionRequest

if TYPE_CHECKING:
    from app.main import app as FastAPI

router = APIRouter()


@router.post("/questions", response_model=List[Question])
async def generate_questions(questions_request: QuestionRequest):
    """
    Генерирует указанное количество вопросов, запрашивая их с публичного API.
    """
    num = questions_request.questions_num
    url = f"https://jservice.io/api/random?count={num}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Ошибка при получении вопросов")

        data = response.json()

        return data


@router.get("/questions", response_model=List[Question])
async def get_questions(page: int = 1, limit: int = 3, app: FastAPI = app_dependency):
    """
    Получает вопросы из базы данных с пагинацией.
    """
    # Calculate the offset based on the page and limit values
    offset = (page - 1) * limit

    # Query the database to fetch questions with pagination
    questions = await app.state.database.execute_query(
        query=select().offset(offset).limit(limit)
    )

    return questions
