import datetime as dt

from pydantic.fields import Field
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator

from src.models.game import Game as GameModel
from src.models.game import StatusEnum


class GameCreate(PydanticModel):
    title: str = Field(max_length=150)
    systems: list[str] = Field(
        default_factory=list, unique_items=True, description="list of systems"
    )
    x_cloud: bool = Field(default=False)
    status: StatusEnum
    date_added: dt.date
    date_removed: dt.date | None
    date_released: dt.date
    genres: list[str] = Field(
        default_factory=list, unique_items=True, description="list of genres' names"
    )
    x_exclusive: bool = Field(default=False)
    esrb_id: str | None

    class Config:
        use_enum_values = True


GameUpdate = pydantic_model_creator(GameModel)

Game = pydantic_model_creator(GameModel)
