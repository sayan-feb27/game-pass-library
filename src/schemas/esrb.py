from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel

from src.models.game import ESRB as ESRBModel


class ESRBUpdate(BaseModel):
    description: str


ESRBCreate = pydantic_model_creator(ESRBModel)
ESRB = pydantic_model_creator(ESRBModel)
