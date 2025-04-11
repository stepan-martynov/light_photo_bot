import asyncio
from pprint import pprint

from dadata import Dadata

from src.configuration import config
# from src.db.database import async_engine, asyng_session_factory, create_tables
# from src.db.models import Agency, Manager, BankAccaunt


class DadataExt(Dadata):
    """Расширение класса Dadata для получения и фильтрации данных о компаниях и банках."""

    def _get_raw_company_data(self, inn: str) -> dict:
        """Получает и фильтрует данные о компании по его ИНН."""
        try:
            return self.find_by_id("party", inn)[0]['data']
        except (KeyError, IndexError, ValueError) as e:
            print(e)
            return None

    def _get_raw_bank_data(self, bik: str) -> dict:
        """Получает и фильтрует данные о банке по его БИК."""
        try:
            return self.find_by_id("bank", bik)[0]['data']
        except (KeyError, IndexError, ValueError) as e:
            print(e)
            return None

    def filter_individual(self, raw_data: dict) -> dict:
        """Фильтрует и форматирует данные индивидуального предпринимателя."""
        individual = {}
        individual['name'] = raw_data['name']['full']
        individual['inn'] = int(raw_data['inn'])
        individual['ogrn'] = int(raw_data['ogrn'])
        individual['opf_short'] = raw_data['opf']['short']
        individual['opf_full'] = raw_data['opf']['full']
        individual['address'] = raw_data['address']['unrestricted_value']
        return individual

    def filter_manager(self, raw_data: dict) -> dict:
        """Фильтрует и форматирует данные о менеджере компании."""
        manager = {}
        manager['full_name'] = raw_data['management']['name']
        manager['post'] = raw_data['management']['post']
        return manager

    def filter_owner(self, raw_data: dict) -> dict:
        """Фильтрует и форматирует данные о владельце компании."""
        owner = {}
        owner['last_name'] = raw_data['fio']['surname']
        owner['name'] = raw_data['fio']['name']
        owner['patronymic'] = raw_data['fio']['patronymic']
        return owner

    def filter_legal(self, raw_data: dict) -> dict:
        """Фильтрует и форматирует данные о юридическом лице."""
        pprint(raw_data)
        company = self.filter_individual(raw_data)
        company['kpp'] = int(raw_data['kpp'])
        return company

    def get_company(self, inn: str) -> tuple[dict, dict]:
        """
        Возвращает кортеж из двух словарей, первый из которых содержит информацию о компании,
        а второй - информацию о ее менеджере или владельце.

        Первый словарь будет содержать ключи "name", "inn", "ogrn", "opf_short", "opf_full",
        "address", и "kpp" если компания является юридическим лицом, или ключи "name", "inn", "ogrn",
        "opf_short", "opf_full", и "address" если компания является индивидуальным предпринимателем.

        Второй словарь будет содержать ключи "full_name", "post" если компания является юридическим лицом,
        или ключи "last_name", "name", "patronymic" если компания является индивидуальным предпринимателем.

        :param inn: ИНН компании
        :return: Кортеж из двух словарей, первый из которых содержит информацию о компании,
                 а второй - информацию о ее менеджере или владельце
        """
        raw_data = self._get_raw_company_data(inn)
        if raw_data["type"] == "LEGAL":
            return self.filter_legal(raw_data), self.filter_manager(raw_data)
        if raw_data["type"] == "INDIVIDUAL":
            return (
                self.filter_individual(raw_data),
                self.filter_owner(raw_data)
            )

    def get_bank_accaunt(self, bik: str) -> dict:
        """Получает и фильтрует данные о банке по его БИК."""
        raw_data = self._get_raw_bank_data(bik)
        bank_accaunt = {}
        bank_accaunt['name'] = raw_data['name']['payment']
        bank_accaunt['bic'] = raw_data['bic']
        bank_accaunt['correspondent_account'] = raw_data['correspondent_account']
        bank_accaunt['address'] = raw_data['address']['unrestricted_value']
        return bank_accaunt


dadata_connection = DadataExt(config.dadata.token)


async def main():
    """Основная функция для тестирования и демонстрации работы класса DadataExt."""
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
    res = dadata_connection.get_company("7839113181")
    pprint(res)
    res = dadata_connection.get_company("7841386500")
    pprint(res)


if __name__ == "__main__":
    asyncio.run(main())
