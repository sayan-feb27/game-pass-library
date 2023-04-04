from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator

from src.models.game import ESRB as ESRBModel

ESRBUpdate = pydantic_model_creator(ESRBModel, exclude_readonly=True)
ESRBCreate = pydantic_model_creator(ESRBModel)


class ESRB(PydanticModel):
    code: str
    description: str
