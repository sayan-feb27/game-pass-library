from fastapi import APIRouter

from .genre import router as genre_router


api_router = APIRouter()
api_router.include_router(genre_router, prefix="/genres", tags=["genres"])
