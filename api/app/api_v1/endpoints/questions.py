from typing import List

import httpx as httpx
from fastapi import HTTPException, APIRouter
from httpx import Response

from api.app.api_v1.deps import app_dependency
from api.app.schemas import QuestionSchema, QuestionRequest


router = APIRouter()


@router.post("/questions", response_model=List[QuestionSchema])
async def generate_questions(questions_request: QuestionRequest, app=app_dependency):
    """
    Генерирует указанное количество вопросов, запрашивая их с публичного API.
    """
    num = questions_request.questions_num

    async def request_questions(num: int) -> Response:
        async with httpx.AsyncClient() as client:
            url = f"https://jservice.io/api/random?count={num}"
            response = await client.get(url)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при получении вопросов",
                )
            return response

    data_out: list[QuestionSchema] = []

    while num > 0:
        data = (await request_questions(num)).json()
        questions_list: List[QuestionSchema] = [
            QuestionSchema(**item) for item in data if item
        ]
        questions_list1 = [
            question
            for question in await app.state.question.add_list_question(questions_list)
            if question
        ]
        num -= len(questions_list1)
        data_out.extend(questions_list1)
    return data_out


@router.get("/questions", response_model=List[QuestionSchema])
async def get_questions(page: int = 1, limit: int = 3, app=app_dependency):
    """
    Получает вопросы из базы данных с пагинацией.
    """

    offset = (page - 1) * limit

    questions = await app.state.question.get_questions_list(limit=limit, offset=offset)

    return questions
