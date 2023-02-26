from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from tortoise.models import Model as DBBaseModel

ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository:
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, obj_id: Any) -> ModelType | None:
        obj = await self._model.filter(pk=obj_id).first()
        return obj

    async def get_multi(self, *, skip=0, limit=100) -> list[ModelType]:
        objs = await self._model.all().offset(skip).limit(limit=limit)
        return objs

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        await db_obj.save()
        return db_obj

    async def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        updated_obj = db_obj.update_from_dict(obj_in_data)
        await updated_obj.save(update_fields=obj_in_data.keys())
        return updated_obj

    async def delete(self, *, obj_id: Any) -> ModelType:
        obj = await self._model.get(pk=obj_id)
        await obj.delete()
        return obj
