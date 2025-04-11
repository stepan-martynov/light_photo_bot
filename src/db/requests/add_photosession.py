from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.db.models.agency import Agency
from src.db.models.contract import Contract
from src.db.models.photographer import Photographer
from src.db.models.photosession import Photosession
from src.db.models.service import Service


async def get_agencies(session: AsyncSession, telegram_id: int) -> list[Agency]:
    """Get list of agencies filtered by photographer's telegram_id"""
    stmt = (
        select(Agency)
        .join(Agency.contracts)
        .join(Contract.photographer)
        .where(Photographer.telegram_id == telegram_id)
        .distinct()
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_services(session: AsyncSession, telegram_id: int) -> list[Service]:
    """Returns a list of services filtered by the photographer's telegram_id"""
    stmt = (
        select(Service)
        .join(Service.photographer)
        .where(Photographer.telegram_id == telegram_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def save_photosession(session: AsyncSession, photo_data: dict) -> Photosession:
    """Save a photosession to the database."""
    agency_id = int(photo_data.pop('agency_id'))
    photographer_telegram_id = photo_data.pop('photographer_id')

    photographer_id = await session.scalar(
        select(Photographer.id).where(Photographer.telegram_id == photographer_telegram_id)
    )

    contract_id = await session.scalar(
        select(Contract.id).where(
            Contract.photographer_id == photographer_id,
            Contract.agency_id == agency_id
        )
    )

    photosession = Photosession(
        date=photo_data['date'],
        url=photo_data['url'],
        location=photo_data['location'],
        price=int(photo_data['price']),
        contract_id=contract_id,
        service_id=int(photo_data['service_id'])
    )

    session.add(photosession)
    await session.commit()
    await session.refresh(photosession)
    return photosession


async def get_photosession_with_details(session: AsyncSession, photosession_id: int, service_id: int) -> Photosession:
    query = select(Photosession).where(Photosession.id == photosession_id).options(
        joinedload(Photosession.contract),
        joinedload(Photosession.contract).joinedload(Contract.photographer),
        joinedload(Photosession.contract).joinedload(Contract.photographer).joinedload(Photographer.services),
        joinedload(Photosession.contract).joinedload(Contract.photographer).joinedload(Photographer.bank_accaunt),
        joinedload(Photosession.contract).joinedload(Contract.agency),
        joinedload(Photosession.contract).joinedload(Contract.agency).joinedload(Agency.bank_accaunt),
        joinedload(Photosession.contract).joinedload(Contract.agency).joinedload(Agency.manager),
        joinedload(Photosession.brocker)).filter(Photosession.service_id == service_id)
    result = await session.execute(query)
    result = result.scalars().first()
    return result
