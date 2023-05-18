from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from starlette.responses import JSONResponse

from api.app.api_v1.deps import app_dependency
from api.app.schemas import ConfigEnv

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}
