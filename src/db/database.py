from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from src.configuration import config
from .models import Manager, BankAccaunt


def create_async_engin(url: str | URL) -> AsyncEngine:
    return _create_async_engine(url=url, echo = config.debug)


def create_session_maker(engine: AsyncEngine | None = None) -> sessionmaker:
    return async_sessionmaker(
        engine or create_async_engin(config.db.connection_str),
        class_=AsyncSession,
        expire_on_commit=False
    )
