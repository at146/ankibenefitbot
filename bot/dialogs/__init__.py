from aiogram import Dispatcher

from . import menu


def include_dialogs(dispatcher: Dispatcher) -> None:
    for dialog in [
        *menu.bot_menu_dialogs(),
    ]:
        dispatcher.include_router(dialog)
