import asyncio
import datetime as dt
import json
from typing import Any

from pydantic import BaseModel, Field
from tortoise import Tortoise

from src.core.settings import TORTOISE_ORM
from src.models.game import ESRB, Game, Genre, StatusEnum, System


class RawGame(BaseModel):
    title: str = Field(alias="Game")
    systems: str | list[str] = Field(alias="System")
    x_cloud: str | bool = Field(default=False, alias="xCloud")
    status: str | StatusEnum = Field(alias="Status")
    date_added: dt.date | str | None = Field(alias="Added", default=None)
    date_removed: dt.date | str | None = Field(alias="Removed", default=None)
    date_released: dt.date | str | None = Field(alias="Release", default=None)
    genres: str | list[str] = Field(alias="Genre (Giantbomb)")
    x_exclusive: str | bool = Field(alias="Xbox Series X|S")
    esrb: str | None = Field(alias="ESRB", default=None)
    esrb_description: str = Field(alias="ESRB Content Descriptors", default="")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.__post_init__()

    def __post_init__(self):
        self.systems = (
            [x.strip() for x in self.systems.split("/") if x] if self.systems else []
        )
        self.x_exclusive = (
            True
            if (
                self.x_exclusive
                and type(self.x_exclusive) == str
                and self.x_exclusive.lower() == "exclusive"
            )
            else False
        )
        self.genres = (
            [x.strip() for x in self.genres.split("/") if x] if self.genres else []
        )
        self.date_added = (
            dt.datetime.strptime(self.date_added, "%b %Y") if self.date_added else None
        )
        self.date_removed = (
            dt.datetime.strptime(self.date_removed, "%b %Y").date()
            if self.date_removed
            else None
        )
        self.date_released = (
            dt.datetime.strptime(self.date_released, "%b %Y").date()
            if self.date_released
            else None
        )
        self.status: StatusEnum = StatusEnum.get_by_value(status=self.status)
        self.x_cloud = (
            True
            if self.x_cloud and self.x_cloud.lower().strip() in ["yes", "1", "true"]
            else False
        )
        self.esrb = self.esrb if self.esrb else None


class JSONLoader:
    def __init__(self, file_path: str):
        self.file_path: str = file_path

    async def load(self):
        await Tortoise.init(config=TORTOISE_ORM)
        # transaction?
        raw_game_data: list[RawGame] = self._read()
        await self.save_systems(raw_data=raw_game_data)
        await self.save_genres(raw_data=raw_game_data)
        await self.save_esrbs(raw_data=raw_game_data)
        await self.save_games(raw_data=raw_game_data)

    def _read(self) -> list[RawGame]:
        with open(self.file_path, "r") as file:
            data = json.load(file)
            return [RawGame(**game) for game in data]

    async def save_systems(self, *, raw_data: list[RawGame]):
        db_systems = []
        for game in raw_data:
            db_systems.extend([System(name=system) for system in game.systems])
        await System.bulk_create(db_systems, batch_size=100, ignore_conflicts=True)

    async def save_genres(self, raw_data: list[RawGame]):
        genres = []
        for game in raw_data:
            genres.extend([Genre(name=genre) for genre in game.genres])
        await Genre.bulk_create(objects=genres, ignore_conflicts=True, batch_size=100)

    async def save_esrbs(self, raw_data: list[RawGame]):
        esrbs = [
            ESRB(code=game.esrb, description=game.esrb_description)
            for game in raw_data
            if game.esrb
        ]
        await ESRB.bulk_create(objects=esrbs, ignore_conflicts=True, batch_size=100)

    async def save_games(self, *, raw_data: list[RawGame]):
        limit, offset = 100, 0
        raw_games = []
        while True:
            batch = raw_data[offset : offset + limit]
            if not batch:
                break

            for raw_game in batch:
                await self.__save_game(raw_game=raw_game)
            offset += limit
            raw_games.extend(batch)
        return raw_games

    async def __save_game(self, raw_game: RawGame):
        game = await Game.create(**raw_game.dict(exclude={"systems", "genres", "esrb"}))
        game.esrb_id = raw_game.esrb

        systems = await System.filter(name__in=raw_game.systems).all()
        genres = await Genre.filter(name__in=raw_game.genres).all()
        await game.systems.add(*systems)
        await game.genres.add(*genres)

        await game.save()


if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file_path", help="path to json raw data")

    args = arg_parser.parse_args()

    loader = JSONLoader(file_path=args.file_path)
    asyncio.run(loader.load())
