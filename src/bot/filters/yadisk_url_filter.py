from typing import Any, Dict
from aiogram.filters import BaseFilter
from aiogram.types import Message


class YadiskUrlFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | Dict[str, Any]:
        entities = message.entities or []
        yadisk_urls = [
            entity
            for item in entities
            if (item.type == "url") and ("disk.yandex.ru" in (entity := item.extract_from(message.text)))
        ]
        if len(yadisk_urls) == 1:
            return {"url": yadisk_urls[0]}
        return False
