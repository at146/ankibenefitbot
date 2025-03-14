from aiogram_dialog import Dialog

from .main import windows as main_windows
from .questioning import windows as questioning_windows
from .result_questioning import callbacks
from .result_questioning import windows as result_questioning_windows


def bot_menu_dialogs() -> list[Dialog]:
    return [
        Dialog(main_windows.main_menu()),
        Dialog(
            *questioning_windows.generate_menu(),
        ),
        Dialog(result_questioning_windows.result_menu(), on_start=callbacks.on_start),
    ]
