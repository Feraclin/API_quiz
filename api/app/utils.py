from typing import List

import httpx
from fastapi import HTTPException
from httpx import Response

from api.app.schemas import QuestionSchema


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


async def generate_question_list(app, data_out, num):
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
