from typing import TYPE_CHECKING

from fastapi import APIRouter, FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from app.api_v1.deps import app_dependency
from app.schemas import ConfigEnv

if TYPE_CHECKING:
    from app.main import app as FastAPI

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/env", response_model=ConfigEnv)
async def view_env(app: FastAPI = app_dependency):
    return app.state.config


@router.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(app: FastAPI = app_dependency):
    """
    Этот эндпоинт генерирует JSON-схему OpenAPI (Swagger).
    """
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="This is the API description",
        routes=app.routes,
    )
    return JSONResponse(content=openapi_schema)
