from typing import TYPE_CHECKING

from fastapi import Depends, Request

if TYPE_CHECKING:
    from app.main import Application


async def get_app(request: Request) -> "Application":
    return request.app


app_dependency = Depends(get_app)
