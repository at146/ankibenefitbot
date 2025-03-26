from aiogram_dialog import Dialog

from .main import windows as main_windows
from .two_menu import callbacks as two_menu_callbacks
from .two_menu import windows as two_menu_windows


def bot_menu_dialogs() -> list[Dialog]:
    return [
        Dialog(main_windows.main_menu()),
        Dialog(two_menu_windows.two_menu(), on_start=two_menu_callbacks.on_start),
    ]
