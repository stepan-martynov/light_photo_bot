from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from src.configuration import config

def async_engin(url: str | URL) -> AsyncEngine:
    return _create_async_engine(url, echo: bool = config.debug)
