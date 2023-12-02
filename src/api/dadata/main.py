import asyncio
from src.configuration import config
import pprint

from dadata import Dadata

dadata = Dadata(config.dadata.token)
keys = [
    "full", 
    "bik", 
    "inn", 
    "kpp", 
    "ogrn", 
    "unrestricted_value",
    "phone", 
    "name",
    "post",
    ]


def agency_by_id(inn: str) -> list:
    try:
        return dadata.find_by_id("party", inn)
    except Exception as e:
        print(e)


def filter_dict(raw_result: dict, keys: list, res: dict = {}) -> dict:
    # pprint.pprint(raw_result)
    for key, value in raw_result.items():
        if isinstance(value, dict):
            filter_dict(value, keys, res)
        elif (key in keys):
            res[key] = value
    try:
        res['opf_full'] = f"{raw_result['opf']['full']}"
        res['opf_short'] = f"{raw_result['opf']['short']}"
        res['manager_post'] = f"{raw_result['management']['post']}".capitalize()
    except:
        ...
    return res


def serilized_agency(inn: str, keys: list) -> dict:
    raw_result = agency_by_id(inn)[0]
    pprint.pprint(raw_result)
    return filter_dict(raw_result, keys)


if __name__ == "__main__":
    pprint.pprint(serilized_agency("7839113181", keys))
