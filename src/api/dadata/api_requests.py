import asyncio
import pprint

from dadata import Dadata
from sqlalchemy import inspect

from src.configuration import config
from src.db.database import *
from src.db.models import Agency, Manager, BankAccaunt


class DadataExt(Dadata):

    def _get_raw_company_data(self, inn: str) -> dict:
        try:
            return self.find_by_id("party", inn)[0]['data']
        except Exception as e:
            print(e)

    def _get_raw_bank_data(self, bik: str) -> dict:
        try:
            return self.find_by_id("bank", bik)[0]['data']
        except Exception as e:
            print(e)

    def filter_individual(self, raw_data: dict) -> dict:
        individual = {}
        individual['name'] = raw_data['name']['full']
        individual['inn'] = int(raw_data['inn'])
        individual['ogrn'] = int(raw_data['ogrn'])
        individual['opf_short'] = raw_data['opf']['short']
        individual['opf_full'] = raw_data['opf']['full']
        individual['address'] = raw_data['address']['unrestricted_value']
        return individual

    def filter_manager(self, raw_data: dict) -> dict:
        manager = {}
        manager['full_name'] = raw_data['management']['name']
        manager['post'] = raw_data['management']['post']
        return manager

    def filter_owner(self, raw_data: dict) -> dict:
        owner = {}
        owner['last_name'] = raw_data['fio']['surname']
        owner['name'] = raw_data['fio']['name']
        owner['patronymic'] = raw_data['fio']['patronymic']
        return owner

    def filter_legal(self, raw_data: dict) -> dict:
        company = self.filter_individual(raw_data)
        company['kpp'] = int(raw_data['kpp'])
        return company

    def get_company(self, inn: str) -> list[dict, dict]:
        raw_data = self._get_raw_company_data(inn)
        if raw_data["type"] == "LEGAL":
            return self.filter_legal(raw_data), self.filter_manager(raw_data)
        if raw_data["type"] == "INDIVIDUAL":
            return self.filter_individual(raw_data), self.filter_owner(raw_data)

    def get_bank_accaunt(self, bik: str) -> dict:
        raw_data = self._get_raw_bank_data(bik)
        bank_accaunt = {}
        bank_accaunt['name'] = raw_data['name']['payment']
        bank_accaunt['bic'] = raw_data['bic']
        bank_accaunt['correspondent_account'] = raw_data['correspondent_account']
        bank_accaunt['address'] = raw_data['address']['unrestricted_value']
        return bank_accaunt


dadata_connection = DadataExt(config.dadata.token)


async def main():
    # await create_tables(async_engine=async_engine)
    # agency, manager = dadata_connection.get_company("7841386500")
    # bank = dadata_connection.get_bank_accaunt("044030706")
    # async with asyng_session_factory() as session:
    #     agency = Agency(**agency)
    #     manager = Manager(**manager)
    #     bank_accaunt = BankAccaunt(**bank)
    #     agency.manager = manager
    #     agency.bank_accaunt = bank_accaunt
    #     session.add_all((agency, manager, bank_accaunt))
    #     await session.commit()

    # bank = dadata_connection._get_raw_bank_data("044030706")
    # res = dadata_connection.get_company("742309106480")
    res = dadata_connection.get_company("7839113181")
    pprint.pprint(res)
    res = dadata_connection.get_company("7841386500")
    pprint.pprint(res)


if __name__ == "__main__":
    asyncio.run(main())
