from collections.abc import Sequence

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db.models import UserLidMagnit


async def get_user_lidmagnit_by_user_id(
    user_id: int, db_session: async_sessionmaker[AsyncSession]
) -> UserLidMagnit | None:
    async with db_session() as session:
        sql = select(UserLidMagnit).where(UserLidMagnit.user_id == user_id)
        return await session.scalar(sql)  # type: ignore


async def insert_user_lidmagnit(
    user_id: int,
    first_name: str,
    username: str | None,
    last_name: str | None,
    db_session: async_sessionmaker[AsyncSession],
) -> None:
    async with db_session() as session:
        sql = insert(UserLidMagnit).values(
            user_id=user_id, first_name=first_name, last_name=last_name, username=username
        )
        await session.execute(sql)
        await session.commit()


async def get_users_lidmagnit(
    db_session: async_sessionmaker[AsyncSession],
) -> Sequence[UserLidMagnit]:
    async with db_session() as session:
        sql = select(UserLidMagnit).order_by(UserLidMagnit.create_datetime)
        execute = await session.scalars(sql)
        return execute.all()


async def get_count(db_session: async_sessionmaker[AsyncSession]) -> int | None:
    async with db_session() as session:
        sql = select(func.count(UserLidMagnit.user_id))
        return await session.scalar(sql)  # type: ignore
