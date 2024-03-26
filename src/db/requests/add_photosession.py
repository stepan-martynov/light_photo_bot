from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.models.agency import Agency
from src.db.models.service import Service

async def get_agencies(session: AsyncSession) -> list[Agency]:
    """Возвращает список агенств"""
    res = await session.execute(select(Agency))
    return res.scalars().all()


async def get_servicies(session: AsyncSession) -> list[Service]:
    """Возвращает список услуг"""
    res = await session.execute(select(Service))
    return res.scalars().all()
