from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from api_v1.temperatures import models


class TemperatureCRUD:
    @staticmethod
    async def get_all_temperatures(
        db: AsyncSession, skip: int = 0, limit: int = 10
    ) -> list[models.Temperature]:
        stmt = (
            select(models.Temperature)
            .options(selectinload(models.Temperature.city))
            .offset(skip)
            .limit(limit)
        )
        result: AsyncResult = await db.execute(stmt)
        return result.scalars().all()


temperature_crud = TemperatureCRUD()
