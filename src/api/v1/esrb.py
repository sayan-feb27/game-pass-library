from fastapi import APIRouter, HTTPException, status

from src.services.esrb import esrb_crud
from src.schemas.esrb import ESRB, ESRBCreate, ESRBUpdate

router = APIRouter()


@router.get("/", response_model=list[ESRB])
async def read_esrbs() -> list[ESRB]:
    """
    Retrieve esrbs.
    """
    esrb = await esrb_crud.get_multi()
    return esrb


@router.get("/{code}", response_model=ESRB)
async def read_esrb(*, code: str) -> ESRB:
    """
    Retrieve a esrb.
    """
    esrb = await esrb_crud.get(obj_id=code)
    return esrb


@router.post("/", response_model=ESRB, status_code=status.HTTP_201_CREATED)
async def create_esrb(
    *,
    esrb_in: ESRBCreate
) -> ESRB:
    """
    Create new a esrb.
    """
    esrb = await esrb_crud.create(obj_in=esrb_in)
    return esrb


@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_esrb(
    *,
    code: str
) -> None:
    """
    Delete a esrb.
    """
    esrb = await esrb_crud.get(obj_id=code)
    if not esrb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await esrb_crud.delete(obj_id=code)
    return


@router.put("/{code}", response_model=ESRB)
async def update_esrb(
    *,
    code: str,
    esrb_in: ESRBUpdate
) -> ESRB:
    """
    Update a esrb.
    """
    db_obj = await esrb_crud.get(obj_id=code)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    esrb = await esrb_crud.update(obj_in=esrb_in, db_obj=db_obj)
    return esrb
