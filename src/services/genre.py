from schemas.genre import GenreCreate, GenreUpdate
from src.models.game import Genre as GenreModel

from .base import RepositoryDB


class RepositoryGenre(RepositoryDB[GenreModel, GenreCreate, GenreUpdate]):
    pass


genre_crud = RepositoryGenre(GenreModel)
