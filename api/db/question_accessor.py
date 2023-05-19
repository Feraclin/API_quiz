import logging
from typing import TYPE_CHECKING, Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.exc import IntegrityError

from api.app.models import Question
from api.app.schemas import QuestionSchema as QuestionSchema

if TYPE_CHECKING:
    from api.db.base import Database


class QuestionAccessor:
    def __init__(self, database: "Database"):
        self.database: "Database" = database
        self.logger: logging.Logger = logging.getLogger("question_accessor")

    async def add_list_question(
        self, lst: list[QuestionSchema]
    ) -> list[bool | Question]:
        """
        Добавляет в базу данных лист вопросов.
        И возвращает добавленные вопросы или False в случае дубликата
        :param lst:
        :return:
        """
        questions = []
        for question_data in lst:
            question = Question.from_schema(question_data)
            self.logger.info(question)
            question = await self.add_question(question=question)
            questions.append(question)
        return questions

    async def get_questions_list(
        self, limit: int, offset: int
    ) -> Sequence[Row | RowMapping | Any]:
        """
        Получает из базы набор вопросов
        :param limit:
        :param offset:
        :return:
        """
        query = select(Question).limit(limit).offset(offset)
        res = await self.database.execute_query(query)
        return res.scalars().all()

    async def add_question(self, question: Question) -> bool | Question:
        """
        Добавляет в базу новый вопрос. Возвращает False в случае дубликата
        :param question:
        :return:
        """
        try:
            await self.database.add_query(question)
            return question
        except IntegrityError as e:
            self.logger.error(f"idx {question.id} already in base. Error: {e}")
            return False
