from fastapi import APIRouter
from api_v1.temperatures import schemas, crud
from dependencies import DbSession


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(db: DbSession):
    return await crud.temperature_crud.get_all_temperatures(db=db)
