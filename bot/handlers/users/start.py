from logging import Logger

from aiogram.types import Message, User
from aiogram_dialog import DialogManager, ShowMode, StartMode
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.crud import users_lidmagnit_db
from bot.dialogs.menu.main.states import BotMenu


async def bot_start(
    message: Message,
    log: Logger,
    event_from_user: User,
    dialog_manager: DialogManager,
    db_session: async_sessionmaker[AsyncSession],
) -> None:
    log.info("[%s] %s: нажал старт", event_from_user.id, event_from_user.full_name)
    user_lidmagnit_db = await users_lidmagnit_db.get_user_lidmagnit_by_user_id(event_from_user.id, db_session)

    if not user_lidmagnit_db:
        await users_lidmagnit_db.insert_user_lidmagnit(
            event_from_user.id,
            event_from_user.first_name,
            event_from_user.username,
            event_from_user.last_name,
            db_session,
        )

    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
