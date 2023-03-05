from schemas.game import GameCreate, GameUpdate
from src.models.game import Game as GameModel

from .base import ModelType, RepositoryDB


class RepositoryGame(RepositoryDB[GameModel, GameCreate, GameUpdate]):
    async def get_multi(self, *, skip=0, limit=100) -> list[ModelType]:
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


game_crud = RepositoryGame(GameModel)
