from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    clues_count: int


class QuestionSchema(BaseModel):
    id: int
    answer: str
    question: str
    value: int
    airdate: datetime
    created_at: datetime
    updated_at: datetime
    category_id: int
    game_id: int
    invalid_count: Optional[int]
    category: Category

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}


class QuestionRequest(BaseModel):
    questions_num: int


class ConfigEnv(BaseModel):
    # DB
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db: str
