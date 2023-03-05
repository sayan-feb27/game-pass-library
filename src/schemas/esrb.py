from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.game import ESRB as ESRBModel

ESRBUpdate = pydantic_model_creator(ESRBModel, exclude_readonly=True)
ESRBCreate = pydantic_model_creator(ESRBModel)
ESRB = pydantic_model_creator(ESRBModel)
