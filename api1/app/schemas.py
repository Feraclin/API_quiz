from datetime import datetime
from pprint import pprint
from typing import Optional
from pydantic import BaseModel, Field
import json


class Category(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    clues_count: int


class Question(BaseModel):
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


# json_data = '[{"id":140055,"answer":"the 80s","question":"Bon Jovi","value":800,"airdate":"2011-06-27T19:00:00.000Z",' \
#             '"created_at":"2022-12-30T20:21:39.333Z","updated_at":"2022-12-30T20:21:39.333Z","category_id":14393,' \
#             '"game_id":3685,"invalid_count":null,"category":{"id":14393,"title":"band debuts by decade",' \
#             '"created_at":"2022-12-30T20:05:07.170Z","updated_at":"2022-12-30T20:05:07.170Z","clues_count":10}}]'
#
# question_dict = json.loads(json_data)
# question = Question(**question_dict[0])
# pprint(question.dict())
