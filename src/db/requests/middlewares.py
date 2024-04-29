from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.models.user import User


async def get_user_role(user_id: int, session: AsyncSession) -> User:
    res = await session.execute(select(User.role).where(User.telegram_id == user_id))
    return res.scalar_one_or_none()
