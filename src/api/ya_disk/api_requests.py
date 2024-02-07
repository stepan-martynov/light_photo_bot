from pprint import pprint
import asyncio
import sys

import yadisk
from src.configuration import config


preview_link = 'https://downloader.disk.yandex.ru/preview/0e0b1455f62fe87d1f22414893eec5dc23111935408e3bd14e362bdd30f49ce3/65bcc456/CWhOTMfDbmFlRaF4iWrZQ23HY_pCBnUNueEeNBCsiHOERyS3J86OkoHhmFUxsG8zt-xntF6GpApCrnCj6KCUOQ%3D%3D?uid=0&filename=20230330_DSC9778.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=L&crop=0'
preview_path = 'test223r4r42.jpg'

client = yadisk.AsyncClient(
    id=config.yadisk.id,
    token=config.yadisk.dev_token
)

async def main():
    async with client:
        await client.download_by_link(preview_link, preview_path)
        print(await client.check_token())
        pprint(await client.get_disk_info())


asyncio.run(main())
