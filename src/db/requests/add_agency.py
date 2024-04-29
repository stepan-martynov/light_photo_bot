from pprint import pprint
from sqlalchemy import select
from src.db.models import BankAccaunt, Agency, Manager, Contract, Photographer
from sqlalchemy.ext.asyncio import AsyncSession


async def save_agency(session: AsyncSession, **data) -> Agency:
    req = await session.execute(select(Photographer).where(Photographer.telegram_id == data['photographer_id']))
    photographer = req.scalar()
    data['agency']['paymant_account'] = data['paymant_account']
    agency = Agency(**data['agency'])
    manager = Manager(**data['manager'])
    bank_account = BankAccaunt(**data['bank'])
    contract = Contract(date=data['contract'], photographer_id=photographer.id)
    agency.manager = manager
    agency.bank_accaunt = bank_account
    agency.contracts.append(contract)
    session.add_all((agency, manager, bank_account))
    await session.commit()
    await session.refresh(agency)
    return agency, manager, bank_account
