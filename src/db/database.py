from sqlalchemy.ext.asyncio import AsyncEngine

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from .models import Base

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.configuration import config
from .models import Manager, BankAccaunt


async_engine: AsyncEngine = create_async_engine(
    url=config.db.connection_str,
    echo=config.debug
)

asyng_session_factory = async_sessionmaker(
    async_engine, expire_on_commit=False)


async def create_tables(async_engine):
    async_engine.echo = False
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_engine.echo = True


if __name__ == "__main__":
    asyncio.run(create_tables(create_async_engine()))
