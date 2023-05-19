from typing import Optional

from fastapi import FastAPI

from api.app.api_v1.deps import app_dependency
from api.app.api_v1.routers import api_router
from api.app.config import config_api
from api.app.schemas import ConfigEnv
from api.db.base import Database
from api.db.question_accessor import QuestionAccessor


class AppState:
    def __init__(self):
        self.database: Optional[Database] = None
        self.config: Optional[ConfigEnv] = None
        self.question: Optional[QuestionAccessor] = None


class Application(FastAPI):
    state: Optional[AppState] = None


app = Application()
app.state = AppState()


@app.on_event("startup")
async def startup_event():
    app.state.config = config_api
    database = Database(app.state.config)
    await database.connect()

    app.state.database = database
    app.state.question = QuestionAccessor(database=app.state.database)


@app.on_event("shutdown")
async def shutdown_event():
    database = app.state.database
    if database:
        await database.disconnect()


app.include_router(router=api_router, prefix="/api", dependencies=[app_dependency])
