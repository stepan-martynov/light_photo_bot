from pprint import pprint
import asyncio
import sys

import yadisk
from src.configuration import config


client = yadisk.AsyncClient(
    id=config.yadisk.id,
    token=config.yadisk.dev_token
)


async def create_dir_flat_list(url, path):
    async with client:
        return await client.get_public_meta(url, path=path, limit=500)


async def create_img_list(url, path='', img_list=[], img_names_list=[]):

    flat_dir_list = await client.get_public_meta(url, path=path, limit=500)

    for item in flat_dir_list.embedded.items:
        if item.type == 'dir':
            await create_img_list(url, ''.join([path, item.path]), img_list, img_names_list)
        elif item.type == 'file' and item.mime_type == "image/jpeg" and (item.name not in img_names_list):
            img_list.append(item)
            img_names_list.append(item.name)
    pprint(img_list)
    pprint(len(img_list))
    return img_list


if __name__ == "__main__":
    asyncio.run(create_img_list("https://disk.yandex.ru/d/hrH-ydWS0GdUgw"))
