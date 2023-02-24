from src.models.game import System as SystemModel
from schemas.system import SystemCreate, SystemUpdate
from .base import RepositoryDB


class RepositorySystem(RepositoryDB[SystemModel, SystemCreate, SystemUpdate]):
    pass


system_crud = RepositorySystem(SystemModel)
