from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine 
from .models import Base

from sqlalchemy.ext.asyncio import async_sessionmaker
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.engine.url import URL

from src.configuration import config
from .models import Manager, BankAccaunt


# def create_async_engine(url: str | URL, echo: bool = config.debug) -> AsyncEngine:
    # return _create_async_engine(url=url, echo=echo)

async_engine = create_async_engine(
     url=config.db.connection_str,
     echo=config.debug
)

asyng_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

# def create_session_maker(engine: AsyncEngine = None) -> sessionmaker:
#     return sessionmaker(
#         engine=engine or create_async_engine(config.db.connection_str),
#         class_=AsyncSession,
#         expire_on_commit=False
#     )


async def create_tables(async_engine):
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


# class Database:
    # session: AsyncSession

if __name__ == "__main__":
    asyncio.run(create_tables(create_async_engine()))