from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.game import Genre as GenreModel

GenreCreate = pydantic_model_creator(GenreModel)
GenreUpdate = pydantic_model_creator(GenreModel)

Genre = pydantic_model_creator(GenreModel)
