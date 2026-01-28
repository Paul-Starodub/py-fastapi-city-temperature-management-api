from datetime import datetime
from typing import Any
from httpx import AsyncClient, HTTPError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from api_v1.cities import models as city_models
from api_v1.temperatures import models as temperature_models


class TemperatureCRUD:
    @staticmethod
    async def _fetch_current_temperature(client: AsyncClient, city_name: str) -> tuple[datetime, float]:
        geocode_resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json",
            },
        )
        geocode_resp.raise_for_status()
        geocode_data: dict[str, Any] = geocode_resp.json()
        results = geocode_data.get("results") or []
        if not results:
            raise ValueError("City not found in geocoding results")
        location = results[0]
        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
        )
        weather_resp.raise_for_status()
        weather_data: dict[str, Any] = weather_resp.json()
        current = weather_data.get("current")
        if not current or "temperature_2m" not in current or "time" not in current:
            raise ValueError("Current temperature data missing")
        return datetime.fromisoformat(current["time"]), float(current["temperature_2m"])

    @staticmethod
    async def _build_temperature_record(
        db: AsyncSession, client: AsyncClient, city: city_models.City
    ) -> temperature_models.Temperature:
        observed_at, temperature = await TemperatureCRUD._fetch_current_temperature(client, city.name)
        record = temperature_models.Temperature(
            city_id=city.id,
            date_time=observed_at,
            temperature=temperature,
        )
        record.city = city
        db.add(record)
        return record

    @staticmethod
    async def get_all_temperatures(
        db: AsyncSession, skip: int = 0, limit: int = 10
    ) -> list[temperature_models.Temperature]:
        stmt = (
            select(temperature_models.Temperature)
            .options(selectinload(temperature_models.Temperature.city))
            .offset(skip)
            .limit(limit)
        )
        result: AsyncResult = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_all_city_temperatures(
        db: AsyncSession,
    ) -> tuple[list[temperature_models.Temperature], dict[str, str]]:
        result: AsyncResult = await db.execute(select(city_models.City))
        cities = result.scalars().all()
        updated: list[temperature_models.Temperature] = []
        failed: dict[str, str] = {}
        async with AsyncClient(timeout=10) as client:
            for city in cities:
                try:
                    record = await TemperatureCRUD._build_temperature_record(db, client, city)
                except (HTTPError, ValueError) as exc:
                    failed[city.name] = str(exc)
                    continue
                updated.append(record)
        if updated:
            try:
                await db.commit()
            except Exception:
                await db.rollback()
                raise
        return updated, failed


temperature_crud = TemperatureCRUD()
