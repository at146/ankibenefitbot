from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Column, Url
from aiogram_dialog.widgets.text import Const

from .states import ResultMenu
from .text import FINISH_TEXT


def result_menu() -> Window:
    return Window(
        Const(FINISH_TEXT),
        Column(
            Url(Const("Открыть статью"), url=Const("https://127.0.0.1")),
            Url(Const("Подписаться на канал"), id="subscribe_channel", url=Const("https://127.0.0.1")),
        ),
        state=ResultMenu.select_result_menu,
    )
