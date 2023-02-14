import pathlib
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)
BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()


class AppSettings(BaseSettings):
    project_name: str = "Stonks"
    project_host: str = "0.0.0.0"
    project_port: int = 8000
    database_dsn: PostgresDsn

    class Config:
        env_file = pathlib.Path(BASE_DIR).joinpath('.env')


app_settings = AppSettings()
