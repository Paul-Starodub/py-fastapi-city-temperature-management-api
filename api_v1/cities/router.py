from fastapi import APIRouter
from api_v1.cities import schemas, crud
from dependencies import DbSession


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: DbSession):
    return await crud.city_crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(db: DbSession, city: schemas.CityCreate):
    return await crud.city_crud.create_city(db=db, city=city)
