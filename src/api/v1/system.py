from fastapi import APIRouter, HTTPException, status

from src.services.system import system_crud
from src.schemas.system import System, SystemCreate

router = APIRouter()


@router.get("/", response_model=list[System])
async def read_systems() -> list[System]:
    """
    Retrieve systems.
    """
    systems = await system_crud.get_multi()
    return systems


@router.get("/{system_name}", response_model=System)
async def read_system(*, system_name: str) -> System:
    """
    Retrieve a system.
    """
    system = await system_crud.get(obj_id=system_name)
    return system


@router.post("/", response_model=System, status_code=status.HTTP_201_CREATED)
async def create_system(
    *,
    system_in: SystemCreate
) -> System:
    """
    Create new a system.
    """
    system = await system_crud.create(obj_in=system_in)
    return system


@router.delete("/{system_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(
    *,
    system_name: str
) -> None:
    """
    Delete a system.
    """
    system = await system_crud.get(obj_id=system_name)
    if not system:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await system_crud.delete(obj_id=system_name)
    return
