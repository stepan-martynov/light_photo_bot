from pprint import pprint
from src.db.models import User, Manager, BankAccaunt, Brocker, Photographer
from sqlalchemy.ext.asyncio import AsyncSession


async def add_user(session: AsyncSession, **user_data) -> User:
    user = User(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def add_brocker(session: AsyncSession, **user_data) -> Brocker:
    brocker = Brocker(**user_data)
    session.add(brocker)
    await session.commit()
    await session.refresh(brocker)
    return brocker


async def save_photographer(session: AsyncSession, **data) -> Photographer:
    bank_account = BankAccaunt(**data['bank'])
    photographer = {k: v for k, v in data.items() if k != 'bank'}
    photographer = Photographer(**photographer)
    photographer.bank_accaunt = bank_account
    session.add_all((photographer, bank_account))
    await session.commit()
    await session.refresh(photographer)
    return photographer
