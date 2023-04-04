from fastapi.encoders import jsonable_encoder

from schemas.game import GameCreate, GameUpdate
from src.models.game import ESRB as ESRBModel
from src.models.game import Game as GameModel
from src.models.game import Genre as GenreModel
from src.models.game import System as SystemModel

from .base import RepositoryDB


class RepositoryGame(RepositoryDB[GameModel, GameCreate, GameUpdate]):
    async def get_multi(self, *, skip=0, limit=100) -> list[GameModel]:
        # todo: add qs method to base class
        # todo: consider returning querysets??
        objs = (
            await self._model.all()
            .offset(skip)
            .limit(limit=limit)
            .prefetch_related("genres", "systems")
            .select_related("esrb")
        )
        return objs

    async def create(self, *, obj_in: GameCreate) -> GameModel:
        obj_in_data = jsonable_encoder(obj_in)

        systems = obj_in_data.pop("systems", [])
        genres = obj_in_data.pop("genres", [])

        db_obj = self._model(**obj_in_data)
        await db_obj.save()

        if systems:
            systems = await SystemModel.filter(name__in=systems)
            await db_obj.systems.add(*systems)
        if genres:
            genres = await GenreModel.filter(name__in=genres)
            await db_obj.genres.add(*genres)

        return db_obj


game_crud = RepositoryGame(GameModel)
