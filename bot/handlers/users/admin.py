from logging import Logger

from aiogram.types import Message, User
from aiogram_dialog import DialogManager, ShowMode, StartMode
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.dialogs.menu.admin.states import AdminMenu


async def command_admin(
    message: Message,
    log: Logger,
    event_from_user: User,
    dialog_manager: DialogManager,
    db_session: async_sessionmaker[AsyncSession],
) -> None:
    await dialog_manager.start(
        AdminMenu.main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
