from typing import List

from fastapi import APIRouter

from api.app.api_v1.deps import app_dependency
from api.app.schemas import QuestionSchema, QuestionRequest
from api.app.utils import generate_question_list

router = APIRouter()


@router.post("/questions", response_model=List[QuestionSchema])
async def generate_questions(questions_request: QuestionRequest, app=app_dependency):
    """
    Генерирует указанное количество вопросов, запрашивая их с публичного API.
    """
    num = questions_request.questions_num

    data_out: list[QuestionSchema] = []

    await generate_question_list(app, data_out, num)
    return data_out


@router.get("/questions", response_model=List[QuestionSchema])
async def get_questions(page: int = 1, limit: int = 3, app=app_dependency):
    """
    Получает вопросы из базы данных с пагинацией.
    """

    offset = (page - 1) * limit

    questions = await app.state.question.get_questions_list(limit=limit, offset=offset)

    return questions
