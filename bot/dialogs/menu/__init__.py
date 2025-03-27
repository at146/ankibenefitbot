from aiogram_dialog import Dialog

from .admin import windows as admin_windows
from .main import windows as main_windows
from .two_menu import callbacks as two_menu_callbacks
from .two_menu import windows as two_menu_windows


def bot_menu_dialogs() -> list[Dialog]:
    return [
        Dialog(main_windows.main_menu()),
        Dialog(two_menu_windows.two_menu(), on_start=two_menu_callbacks.on_start),
        Dialog(
            admin_windows.main_menu(),
            admin_windows.spam_menu(),
            admin_windows.text_spam_menu(),
            admin_windows.result_spam_menu(),
        ),
    ]
