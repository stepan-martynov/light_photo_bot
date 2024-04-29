from pprint import pprint
from typing import Any, Dict
from aiogram.filters import BaseFilter


class UserRoleFilter(BaseFilter):
    def __init__(self, user_role: str | list[str]) -> None:
        self.user_role = user_role

    async def __call__(self, *args: Any, **data: Any) -> bool:
        if isinstance(self.user_role, list):
            return data['role'] in self.user_role
        else:
            return data['role'] == self.user_role
