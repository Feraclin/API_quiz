from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import MappedAsDataclass, mapped_column, Mapped, relationship

from app.schemas import QuestionSchema
from db.base_class import Base


class Category(MappedAsDataclass, Base):
    """
    Класс, представляющий категорию.

    :param id: Идентификатор категории.
    :param title: Заголовок категории.
    :param created_at: Дата и время создания.
    :param updated_at: Дата и время обновления.
    :param clues_count: Количество подсказок.
    """
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
    clues_count: Mapped[int] = mapped_column()


class Question(MappedAsDataclass, Base):
    """
    Класс, представляющий вопрос.

    :param id: Идентификатор вопроса.
    :param answer: Ответ на вопрос.
    :param question: Текст вопроса.
    :param value: Значение вопроса.
    :param airdate: Дата и время вопроса.
    :param created_at: Дата и время создания.
    :param updated_at: Дата и время обновления.
    :param category_id: Идентификатор категории.
    :param game_id: Идентификатор игры.
    :param invalid_count: Количество недействительных вопросов.
    :param category: Категория вопроса.
    """
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str] = mapped_column()
    question: Mapped[str] = mapped_column()
    value: Mapped[int] = mapped_column()
    airdate: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), onupdate="CASCADE")
    game_id: Mapped[int] = mapped_column()
    invalid_count: Mapped[int] = mapped_column()
    category: Mapped[Category] = relationship(Category, lazy="joined", foreign_keys=[category_id])

    @classmethod
    def from_schema(cls, schema: QuestionSchema) -> "Question":
        category = Category(id=schema.category.id,
                            title=schema.category.title,
                            created_at=schema.category.created_at.replace(tzinfo=None),
                            updated_at=schema.category.updated_at.replace(tzinfo=None),
                            clues_count=schema.category.clues_count)
        question = Question(
            id=schema.id,
            answer=schema.answer,
            question=schema.question,
            value=schema.value,
            airdate=schema.airdate.replace(tzinfo=None),
            created_at=schema.created_at.replace(tzinfo=None),
            updated_at=schema.updated_at.replace(tzinfo=None),
            category_id=schema.category_id,
            game_id=schema.game_id,
            invalid_count=0,
            category=category)
        return question
