from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
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

    async def get(self, obj_id: Any) -> Optional[ModelType]:
        # TODO:
        pass

    async def get_multi(self, *, skip=0, limit=100) -> List[ModelType]:
        # TODO:
        pass

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        # TODO:
        pass

    async def update(self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        # TODO:
        pass

    async def delete(self, *, obj_id: int) -> ModelType:
        # TODO:
        pass
