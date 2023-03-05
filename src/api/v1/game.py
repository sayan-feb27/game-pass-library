import http

from fastapi import APIRouter, HTTPException, status

from src.schemas.game import Game, GameCreate, GameUpdate
from src.services.game import game_crud

router = APIRouter()


@router.get("/", response_model=list[Game])
async def read_games(skip: int = 0, limit: int = 100) -> list[Game]:
    games = await game_crud.get_multi(skip=skip, limit=limit)
    return games


@router.get("/{game_id}", response_model=Game)
async def read_game(game_id: int) -> Game:
    game = await game_crud.get(obj_id=game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    await game.fetch_related("genres", "systems", "esrb")
    return game


@router.post("/", response_model=Game, status_code=http.HTTPStatus.CREATED)
async def create_game(game_in: GameCreate) -> Game:
    game = await game_crud.create(obj_id=game_in)
    return game


@router.put("/{game_id}", response_model=Game, status_code=http.HTTPStatus.CREATED)
async def update_game(game_id: int, game_in: GameUpdate) -> Game:
    game = await game_crud.create(obj_id=game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    updated_game = await game_crud.update(db_obj=game, obj_in=game_in)
    return updated_game


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(*, game_id: int) -> None:
    """
    Delete a esrb.
    """
    game = await game_crud.get(obj_id=game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    await game_crud.delete(obj_id=game_id)
    return
