from fastapi import APIRouter, HTTPException, status

from src.schemas.genre import Genre, GenreCreate
from src.services.genre import genre_crud

router = APIRouter()


@router.get("/", response_model=list[Genre])
async def read_genres() -> list[Genre]:
    """
    Retrieve genres.
    """
    genres = await genre_crud.get_multi()
    return genres


@router.get("/{genre_name}", response_model=Genre)
async def read_genre(*, genre_name: str) -> Genre:
    """
    Retrieve genre.
    """
    genre = await genre_crud.get(obj_id=genre_name)
    return genre


@router.post("/", response_model=Genre, status_code=status.HTTP_201_CREATED)
async def create_genre(*, genre_in: GenreCreate) -> Genre:
    """
    Create new genre.
    """
    genre = await genre_crud.create(obj_in=genre_in)
    return genre


@router.delete("/{genre_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(*, genre_name: str) -> None:
    """
    Delete a genre.
    """
    genre = await genre_crud.get(obj_id=genre_name)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    await genre_crud.delete(obj_id=genre_name)
    return
