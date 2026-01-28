from fastapi import APIRouter
from api_v1.temperatures import schemas, crud
from api_v1.dependencies import DbSession, Skip, Limit


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(db: DbSession, skip: Skip = 0, limit: Limit = 100):
    return await crud.temperature_crud.get_all_temperatures(
        db=db, skip=skip, limit=limit
    )


@router.post("/temperatures/update/", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: DbSession):
    updated, failed = await crud.temperature_crud.update_all_city_temperatures(db=db)
    return schemas.TemperatureUpdateResult(updated=updated, failed=failed)
