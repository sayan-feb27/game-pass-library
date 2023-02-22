from fastapi import APIRouter, Depends, HTTPException, status

from src.services.genre import genre_crud
from src.schemas.genre import Genre

router = APIRouter()


@router.get("/", response_model=list[Genre])
async def read_genres(skip: int = 0, limit: int = 50) -> list[Genre]:
    """
    Retrieve genres.
    """
    genres = await genre_crud.get_multi(skip=skip, limit=limit)
    return genres


@router.get("/{genre_name}", response_model=Genre)
async def read_genre(*, genre_name: str) -> Genre:
    """
    Retrieve genres.
    """
    genre = await genre_crud.get(obj_id=genre_name)
    return genre
