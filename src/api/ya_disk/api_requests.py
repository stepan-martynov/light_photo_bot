from typing import NamedTuple
from pprint import pprint
import asyncio
import sys
import random

import yadisk
from yadisk.objects.resources import AsyncPublicResourceObject
from src.configuration import config


# client = yadisk.AsyncClient(
    # id=config.yadisk.id,
    # token=config.yadisk.dev_token
# )


async def get_yadisk_client() -> yadisk.AsyncClient:

    return yadisk.AsyncClient(
        id=config.yadisk.id,
        token=config.yadisk.dev_token
    )


class YD_image(NamedTuple):
    name: str
    preview: str


async def create_dir_flat_list(url: str, path: str) -> AsyncPublicResourceObject:
    async with client:
        return await client.get_public_meta(url, path=path, limit=500, preview_size='L')


async def create_img_list(yadisk_client: yadisk.AsyncClient, url: str, path='', img_list=[], img_names_list=[]) -> list[YD_image]:
    flat_dir_list = await yadisk_client.get_public_meta(url, path=path, limit=500, preview_size='L')

    for item in flat_dir_list.embedded.items:
        if item.type == 'dir':
            await create_img_list(yadisk_client, url, ''.join([path, item.path]), img_list, img_names_list)
        elif item.type == 'file' and item.mime_type == "image/jpeg" and (item.name not in img_names_list):
            img = YD_image(item.name, item.preview)
            img_list.append(img)
            img_names_list.append(item.name)
    return img_list


async def get_date_from_imglist(img_list: list[YD_image]) -> str:
    return random.choice(img_list).name[:8]


async def get_location(client: yadisk.AsyncClient, url: str) -> str:
    async with client:
        dir_info = await client.get_public_meta(url, path='', fields=['name', ])

    return dir_info.name.lstrip('0123456789.- ')


async def main():
    # url = "https://disk.yandex.ru/d/YYRBWB7jnHmmrA"
    url = "https://disk.yandex.ru/d/8Bts6G0pcnnoMA"
    dir_name = await get_location(url)
    print(dir_name.lstrip('0123456789.- '))

    # img_list = await create_img_list("https://disk.yandex.ru/d/YYRBWB7jnHmmrA")
    # pprint(img_list)
    # print(await get_date_from_imglist(img_list))

if __name__ == "__main__":
    asyncio.run(main())
