import logging
from logging import Logger

from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager, ShowMode, StartMode

from .main.states import BotMenu


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    # Example of handling UnknownIntent Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_unknown_state(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    # Example of handling UnknownState Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def errors_handler(event: ErrorEvent, log: Logger) -> None:
    log.critical("Critical error caused by %s", event.exception, exc_info=True)
