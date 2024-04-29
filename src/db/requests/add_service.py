from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.photographer import Photographer
from src.db.models.service import Service


async def add_service(session: AsyncSession, service: dict, telegram_id: int) -> Service:
    service = Service(**service)
    photographer = await session.execute(select(Photographer).where(Photographer.telegram_id == telegram_id))
    service.photographer = photographer.scalars().first()
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service
