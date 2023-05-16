from fastapi import FastAPI

from app.api_v1.deps import app_dependency
from app.api_v1.routers import api_router
from app.config import config_api
from app.schemas import ConfigEnv
from db.base import Database


class AppState:
    def __init__(self):
        self.database: Database = None
        self.config: ConfigEnv = None


app = FastAPI()
app.state = AppState()


@app.on_event("startup")
async def startup_event():
    app.state.config = config_api
    database = Database(app.state.config)
    await database.connect()
    # Store the database instance in the app for dependency injection
    app.state.database = database


@app.on_event("shutdown")
async def shutdown_event():
    database = app.state.database
    if database:
        await database.disconnect()


app.include_router(router=api_router,
                   prefix="/api_v1",
                   dependencies=[app_dependency])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
