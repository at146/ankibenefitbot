from logging import Logger

from aiogram.types import Chat, ChatJoinRequest, User
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.core.config import settings
from bot.crud import users_channel_db


async def bot_chat_join_request(
    chat_join_request: ChatJoinRequest,
    log: Logger,
    event_from_user: User,
    event_chat: Chat,
    db_session: async_sessionmaker[AsyncSession],
    # **kwargs,
) -> None:
    log.info(
        "[%s] %s: перешел по ссылке с подтверждением в канал (full_name - %s, id - %s)",
        event_from_user.id,
        event_from_user.full_name,
        event_chat.full_name,
        event_chat.id,
    )
    # Подписываем пользователя на канал
    # aiogram.exceptions.TelegramBadRequest: Telegram server says - Bad Request: USER_ALREADY_PARTICIPANT
    check_approve = await chat_join_request.approve()
    if not check_approve:
        log.error(
            "[%s] %s: Ошибка при подтверждении пользователя в канал (full_name - %s, id - %s)",
            event_from_user.id,
            event_from_user.full_name,
            event_chat.full_name,
            event_chat.id,
        )
        return

    if event_chat.id == settings.GOOGLE_SHEET_TELEGRAM_CHANNEL_ID:
        await users_channel_db.insert_user_channel(
            event_from_user.id,
            event_from_user.first_name,
            event_from_user.username,
            event_from_user.last_name,
            db_session,
        )
