import asyncio
import pprint

from dadata import Dadata
from sqlalchemy import inspect

from src.configuration import config
from src.db.database import *
from src.db.models import Agency, Manager, BankAccaunt


class DadataExt(Dadata):

    def _get_raw_agency_data(self, inn: str) -> dict:
        try:
            return self.find_by_id("party", inn)[0]['data']
        except Exception as e:
            print(e)

    def _get_raw_bank_data(self, bik: str) -> dict:
        try:
            return self.find_by_id("bank", bik)[0]['data']
        except Exception as e:
            print(e)

    def get_agency(self, raw_data: dict) -> dict:
        agency = {}
        agency['name'] = raw_data['name']['full']
        agency['inn'] = int(raw_data['inn'])
        agency['kpp'] = int(raw_data['kpp'])
        agency['ogrn'] = int(raw_data['ogrn'])
        agency['opf_short'] = raw_data['opf']['short']
        agency['opf_full'] = raw_data['opf']['full']
        agency['address'] = raw_data['address']['unrestricted_value']
        return agency

    def get_manager(self, raw_data: dict) -> dict:
        manager = {}
        manager['full_name'] = raw_data['management']['name']
        manager['post'] = raw_data['management']['post']
        return manager

    def get_company(self, inn: str) -> (dict, dict):
        raw_data = self._get_raw_agency_data(inn)
        return self.get_agency(raw_data), self.get_manager(raw_data)

    def get_bank_accaunt(self, bik: str) -> dict:
        raw_data = self._get_raw_bank_data(bik)
        bank_accaunt = {}
        bank_accaunt['name'] = raw_data['name']['payment']
        bank_accaunt['bic'] = int(raw_data['bic'])
        bank_accaunt['address'] = raw_data['address']['unrestricted_value']
        return bank_accaunt


dadata_connection = DadataExt(config.dadata.token)


async def main():
    await create_tables(async_engine=async_engine)
    agency, manager = dadata_connection.get_company("7841386500")
    bank = dadata_connection.get_bank_accaunt("044030706")
    async with asyng_session_factory() as session:
        agency = Agency(**agency)
        manager = Manager(**manager)
        bank_accaunt = BankAccaunt(**bank)
        agency.manager = manager
        agency.bank_accaunt = bank_accaunt
        session.add_all((agency, manager, bank_accaunt))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
