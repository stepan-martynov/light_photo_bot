import asyncio
import pprint

from dadata import Dadata
from sqlalchemy import inspect

from src.configuration import config
from src.db.database import *
from src.db.models import Agency, Manager, BankAccaunt


dadata = Dadata(config.dadata.token)


def get_raw_data(inn: str) -> dict:
    try:
        return dadata.find_by_id("party", inn)[0]['data']
    except Exception as e:
        print(e)


def get_agency(raw_data: dict) -> dict:

    agency = {}
    agency['name'] = raw_data['name']['full']
    agency['inn'] = int(raw_data['inn'])
    agency['kpp'] = int(raw_data['kpp'])
    agency['ogrn'] = raw_data['ogrn']
    agency['opf_short'] = raw_data['opf']['short']
    agency['opf_full'] = raw_data['opf']['full']
    agency['address'] = raw_data['address']['unrestricted_value']
    pprint.pprint(agency)
    return agency


def get_manager(raw_data: dict) -> dict:
    manager = {}
    manager['full_name'] = raw_data['management']['name']
    manager['post'] = raw_data['management']['post']
    pprint.pprint(manager)
    return manager


async def main():
    await create_tables(async_engine=async_engine)
    raw_data = get_raw_data("7839113181")
    # pprint.pprint(raw_data)
    agency = get_agency(raw_data)
    manager = get_manager(raw_data)
    async with asyng_session_factory() as session:
        agency = Agency(**agency)
        manager = Manager(**manager)
        agency.manager.append(manager)
        session.add(manager)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
