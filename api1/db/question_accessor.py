import logging
from typing import TYPE_CHECKING

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from app.models import Question
from app.schemas import QuestionSchema as QuestionSchema
if TYPE_CHECKING:
    from db.base import Database


class QuestionAccessor:
    def __init__(self, database: "Database"):
        self.database: "Database" = database
        self.logger: logging.Logger = logging.getLogger("question_accessor")

    async def add_list_question(self, lst: list[QuestionSchema]) -> list[bool | Question]:
        questions = []
        for question_data in lst:

            question = Question.from_schema(question_data)
            print(question)
            question = await self.add_question(question=question)

            questions.append(question)
        return questions

    async def get_questions_list(self, limit: int, offset: int) -> list[Question]:
        query = select(Question).limit(limit).offset(offset)
        res = await self.database.execute_query(query)
        return res.scalars().all()

    async def add_question(self, question: Question) -> bool | Question:
        try:
            await self.database.add_query(question)
            return question
        except IntegrityError as e:
            print(e)
            self.logger.error("%idx question already in base".format(idx=question.id))
            return False
