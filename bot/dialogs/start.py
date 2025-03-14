from logging import Logger

from aiogram.types import Message, User
from aiogram_dialog import DialogManager, ShowMode, StartMode

from bot.dialogs.menu.main.states import BotMenu


async def bot_start(message: Message, log: Logger, event_from_user: User, dialog_manager: DialogManager) -> None:
    log.info("[%s] %s: нажал старт", event_from_user.id, event_from_user.full_name)
    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
