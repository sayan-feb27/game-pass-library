from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.game import Game as GameModel

# TODO: write custom
GameCreate = pydantic_model_creator(GameModel)
GameUpdate = pydantic_model_creator(GameModel)

Game = pydantic_model_creator(GameModel)
