from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db.models import User


async def get_user_by_user_id(user_id: int, db_session: async_sessionmaker[AsyncSession]) -> User | None:
    async with db_session() as session:
        sql = select(User).where(User.user_id == user_id)
        return await session.scalar(sql)  # type: ignore


async def insert_user(
    user_id: int,
    first_name: str,
    username: str | None,
    last_name: str | None,
    db_session: async_sessionmaker[AsyncSession],
) -> User:
    async with db_session() as session:
        user = User()
        user.user_id = user_id
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        session.add(user)
        await session.commit()
        return user


async def get_users(
    db_session: async_sessionmaker[AsyncSession],
) -> Sequence[User]:
    async with db_session() as session:
        sql = select(User).order_by(User.create_datetime)
        execute = await session.scalars(sql)
        return execute.all()
