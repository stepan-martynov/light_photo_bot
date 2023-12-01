from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine.url import URL

from src.configuration import config

engin = create_async_engine(
    url: URL = config.db.connection_str,
)