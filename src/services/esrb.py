from src.models.game import ESRB as ESRBModel
from schemas.esrb import ESRBCreate, ESRBUpdate
from .base import RepositoryDB


class RepositoryESRB(RepositoryDB[ESRBModel, ESRBCreate, ESRBUpdate]):
    pass


esrb_crud = RepositoryESRB(ESRBModel)
