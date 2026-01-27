from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.cities import models, schemas


class CityCRUD:
    @staticmethod
    async def get_all_cities(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[models.City]:
        stmt = select(models.City).order_by(models.City.name).offset(skip).limit(limit)
        result: Result = await db.execute(stmt)
        cities = result.scalars().all()
        return list(cities)

    @staticmethod
    async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
        return await db.get(models.City, city_id)

    @staticmethod
    async def create_city(db: AsyncSession, city_create: schemas.CityCreate) -> models.City:
        city = models.City(**city_create.model_dump())
        db.add(city)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City with this name already exists")
        await db.refresh(city)
        return city

    @staticmethod
    async def update_city(db: AsyncSession, city_id: int, city_update: schemas.CityUpdate) -> models.City | None:
        existing_city = await db.scalar(
            select(models.City).where(models.City.name == city_update.name).where(models.City.id != city_id)
        )
        if existing_city:
            raise HTTPException(400, "City name must be unique")
        city = await db.get(models.City, city_id)
        if city is None:
            return None
        city.name = city_update.name
        city.additional_info = city_update.additional_info
        await db.commit()
        return city

    @staticmethod
    async def patch_city(db: AsyncSession, city_id: int, city_patch: schemas.CityPartialUpdate) -> models.City | None:
        city = await db.get(models.City, city_id)
        if city is None:
            return None
        update_data = city_patch.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing_city = await db.scalar(
                select(models.City).where(models.City.name == update_data["name"]).where(models.City.id != city_id)
            )
            if existing_city:
                raise HTTPException(400, "City name must be unique")
        for field, value in update_data.items():
            setattr(city, field, value)
        await db.commit()
        return city

    @staticmethod
    async def delete_city(db: AsyncSession, city_id: int) -> models.City | None:
        city = await db.get(models.City, city_id)
        if city is None:
            return None
        await db.delete(city)
        await db.commit()
        return city


city_crud = CityCRUD()
