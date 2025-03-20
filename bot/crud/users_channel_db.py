from collections.abc import Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db.models import UserChannel


async def insert_user_channel(
    user_id: int,
    first_name: str,
    username: str | None,
    last_name: str | None,
    db_session: async_sessionmaker[AsyncSession],
) -> None:
    async with db_session() as session:
        sql = insert(UserChannel).values(user_id=user_id, first_name=first_name, last_name=last_name, username=username)
        await session.execute(sql)
        await session.commit()


async def get_users_channel(
    db_session: async_sessionmaker[AsyncSession],
) -> Sequence[UserChannel]:
    async with db_session() as session:
        sql = select(UserChannel).order_by(UserChannel.create_datetime)
        execute = await session.scalars(sql)
        return execute.all()
