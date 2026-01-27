from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()
