from fastapi import APIRouter

from .genre import router as genre_router
from .system import router as system_router


api_router = APIRouter()
api_router.include_router(genre_router, prefix="/genres", tags=["genres"])
api_router.include_router(system_router, prefix="/systems", tags=["systems"])
