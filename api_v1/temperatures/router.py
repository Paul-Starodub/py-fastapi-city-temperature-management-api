from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.temperatures import schemas, crud
from dependencies import get_db


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.temperature_crud.get_all_temperatures(db=db)
