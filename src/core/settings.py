import pathlib
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn
from tortoise import Tortoise

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)
BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()


class AppSettings(BaseSettings):
    project_name: str = "GamePass Library"
    database_dsn: PostgresDsn

    class Config:
        env_file = pathlib.Path(BASE_DIR).joinpath(".env")


app_settings = AppSettings()

TORTOISE_ORM = {
    "connections": {"default": app_settings.database_dsn},
    "apps": {
        "models": {
            "models": ["src.models.game", "aerich.models"],
            "default_connection": "default",
        },
    },
}

Tortoise.init_models(TORTOISE_ORM["apps"]["models"]["models"], "models")
