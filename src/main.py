from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from core.settings import app_settings, TORTOISE_ORM
from api.v1.base import api_router


app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

register_tortoise(
    app,
    config=TORTOISE_ORM,
    add_exception_handlers=True
)
