from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from api_v1.cities import models, schemas


class CityCRUD:
    @staticmethod
    async def get_all_cities(
        db: AsyncSession, skip: int = 0, limit: int = 10
    ) -> list[models.City]:
        stmt = select(models.City).offset(skip).limit(limit)
        result: AsyncResult = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
        stmt = models.City(**city.model_dump())
        db.add(stmt)
        await db.commit()
        await db.refresh(stmt)
        return stmt


city_crud = CityCRUD()
