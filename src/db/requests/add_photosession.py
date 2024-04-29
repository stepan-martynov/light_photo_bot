from pprint import pprint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.models.agency import Agency
from src.db.models.contract import Contract
from src.db.models.photographer import Photographer
from src.db.models.photosession import Photosession
from src.db.models.service import Service

async def get_agencies(session: AsyncSession) -> list[Agency]:
    """Возвращает список агенств"""
    res = await session.execute(select(Agency))
    return res.scalars().all()


async def get_servicies(session: AsyncSession, telegram_id) -> list[Service]:
    """Возвращает список услуг"""
    res = await session.execute(select(Service).where(Photographer.telegram_id == telegram_id))
    return res.scalars().all()


async def save_photosession(session: AsyncSession, photo_data) -> Photosession:
    """Сохраняем фотосессию"""
    agency_id = int(photo_data.pop('agency_id'))
    photographer = photo_data.pop('photographer_id')
    res = await session.execute(select(Photographer.id).where(Photographer.telegram_id == photographer))
    photographer = res.scalar_one_or_none()
    print(photographer)
    res = await session.execute(select(Contract.id).where(Contract.photographer_id == photographer, Contract.agency_id == agency_id))
    contract_id = res.scalars().first()
    service_id = photo_data.pop('service_id')
    pprint(photo_data)
    pprint(contract_id)
    photosession = Photosession(
        date=photo_data['date'],
        url=photo_data['url'],
        location=photo_data['location'],
        price=int(photo_data['price']),
        contract_id=int(contract_id),
    )
    session.add(photosession)
    await session.commit()
    await session.refresh(photosession)
