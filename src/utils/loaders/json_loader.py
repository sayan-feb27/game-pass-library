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
    status: StatusEnum | str = Field(alias="Status")
    date_added: dt.date | str | None = Field(alias="Added", default=None)
    date_removed: dt.date | str | None = Field(alias="Removed", default=None)
    date_released: dt.date | str | None = Field(alias="Release", default=None)
    genres: str | list[str] = Field(alias="Genre (Giantbomb)")
    x_exclusive: str | bool = Field(alias="Xbox Series X|S")
    esrb: str | None = Field(alias="ESRB", default=None)
    # TODO: esrb_description

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
        self.status = StatusEnum.get_by_value(status=self.status)
        self.x_cloud = (
            True
            if self.x_cloud and self.x_cloud.lower().strip() in ["yes", "1", "true"]
            else False
        )
        self.esrb = self.esrb if self.esrb else None


class GenreLoaderMixin:
    def extract_genres(self, raw_game_data: list[dict[str, Any]]) -> set[str]:
        result = set()
        genre_key = None
        for data in raw_game_data:
            genre_key = genre_key or next(
                (x for x in data.keys() if x.lower().startswith("genre")), None
            )
            if genre_key is None:
                raise Exception("Failed to find genre key in provided data.")
            game_genres = {x.strip() for x in data[genre_key].split("/") if x}
            result = result.union(game_genres)
        return result

    async def save_genres(self, genres: set[str]):
        tasks = [Genre(name=genre).save() for genre in genres]
        await asyncio.gather(*tasks)


class SystemLoaderMixin:
    def extract_systems(self, raw_game_data: list[dict[str, Any]]) -> set[str]:
        result = set()
        for data in raw_game_data:
            game_systems = {x.strip() for x in data["System"].split("/") if x}
            result = result.union(game_systems)
        return result

    async def save_systems(self, systems: set[str]):
        tasks = [System(name=system).save() for system in systems]
        await asyncio.gather(*tasks)


class ESRBLoaderMixin:
    def extract_esrb(self, raw_game_data: list[dict[str, Any]]) -> list[dict[str, str]]:
        result = []
        codes = set()
        for data in raw_game_data:
            code, description = data["ESRB"], data["ESRB Content Descriptors"]
            if not code or code in codes:
                continue
            esrb = {"code": code, "description": description}
            result.append(esrb)
            codes.add(code)
        return result

    async def save_esrb(self, esrb_data: list[dict[str, str]]):
        tasks = [
            ESRB(code=esrb["code"], description=esrb["description"]).save(
                force_update=True
            )
            for esrb in esrb_data
        ]
        await asyncio.gather(*tasks)


class GameLoaderMixin:
    async def save_games(self, raw_data: list[dict[str, str]]):
        limit, offset = 100, 0
        raw_games = []
        while True:
            batch = raw_data[offset : offset + limit]
            if not batch:
                break

            batch_raw_games = [RawGame(**game) for game in batch]
            for raw_game in batch_raw_games:
                await self.save_game(raw_game=raw_game)
            offset += limit
            raw_games.extend(batch_raw_games)
        return raw_games

    async def save_game(self, raw_game: RawGame):
        game = await Game.create(**raw_game.dict(exclude={"systems", "genres", "esrb"}))
        game.esrb_id = raw_game.esrb

        # TODO: keep records of created
        # TODO: create if not exists
        systems = await System.filter(name__in=raw_game.systems).all()
        genres = await Genre.filter(name__in=raw_game.genres).all()
        await game.systems.add(*systems)
        await game.genres.add(*genres)

        await game.save()


class JSONLoader(GenreLoaderMixin, SystemLoaderMixin, ESRBLoaderMixin, GameLoaderMixin):
    # TODO: enum
    GENRE = "GENRE"
    SYSTEM = "SYSTEM"
    ESRB = "ESRB"
    GAME = "GAME"
    MODELS = [GAME, GENRE, SYSTEM, ESRB]

    def __init__(self, file_path: str, model: str):
        self.file_path: str = file_path
        self.model: str = model.upper()
        if self.model not in self.MODELS:
            raise Exception(f"Unknown mode {self.model}")

    async def load(self):
        await Tortoise.init(config=TORTOISE_ORM)
        raw_game_data: list[dict[str, Any]] = self._read()
        # TODO: simplify
        match self.model:
            case self.GENRE:
                genres: set[str] = self.extract_genres(raw_game_data)
                await self.save_genres(genres=genres)
            case self.SYSTEM:
                systems: set[str] = self.extract_systems(raw_game_data)
                await self.save_systems(systems=systems)
            case self.ESRB:
                esrb_data: list[dict[str, str]] = self.extract_esrb(raw_game_data)
                await self.save_esrb(esrb_data=esrb_data)
            case self.GAME:
                raw_games = await self.save_games(raw_game_data)
                print(raw_games)
            case _:
                pass

    def _read(self) -> list[dict[str, Any]]:
        with open(self.file_path, "r") as file:
            data = json.load(file)
            return data


if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file_path", help="path to json raw data")
    arg_parser.add_argument("model", help="model to load")

    args = arg_parser.parse_args()

    loader = JSONLoader(file_path=args.file_path, model=args.model)
    asyncio.run(loader.load())
