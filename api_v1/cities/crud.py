from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from api_v1.cities import models


class CityCRUD:
    @staticmethod
    async def get_all_cities(
        db: AsyncSession, skip: int = 0, limit: int = 10
    ) -> list[models.City]:
        stmt = select(models.City).offset(skip).limit(limit)
        result: AsyncResult = await db.execute(stmt)
        return result.scalars().all()


city_crud = CityCRUD()
