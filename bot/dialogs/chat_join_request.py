from logging import Logger

from aiogram.types import ChatJoinRequest, User
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.crud import users_channel_db


async def bot_chat_join_request(
    chat_join_request: ChatJoinRequest,
    log: Logger,
    event_from_user: User,
    db_session: async_sessionmaker[AsyncSession],
) -> None:
    log.info("[%s] %s: перешел ссылке с подтверждением в канал", event_from_user.id, event_from_user.full_name)
    if await chat_join_request.approve():
        await users_channel_db.insert_user_channel(
            event_from_user.id,
            event_from_user.first_name,
            event_from_user.username,
            event_from_user.last_name,
            db_session,
        )
    else:
        log.error(
            "[%s] %s: Ошибка при подтверждении пользователя в канал", event_from_user.id, event_from_user.full_name
        )
