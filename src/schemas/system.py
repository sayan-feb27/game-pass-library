from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.game import System as SystemModel

SystemCreate = pydantic_model_creator(SystemModel)
SystemUpdate = pydantic_model_creator(SystemModel)

System = pydantic_model_creator(SystemModel)
