from fastapi import APIRouter

from .esrb import router as esrb_router
from .game import router as game_router
from .genre import router as genre_router
from .system import router as system_router

api_router = APIRouter()
api_router.include_router(genre_router, prefix="/genres", tags=["genres"])
api_router.include_router(system_router, prefix="/systems", tags=["systems"])
api_router.include_router(esrb_router, prefix="/esrb", tags=["esrb"])
api_router.include_router(game_router, prefix="/games", tags=["games"])
