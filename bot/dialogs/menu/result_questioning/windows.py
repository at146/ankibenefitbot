from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Column, Url
from aiogram_dialog.widgets.text import Const

from bot.core.config import settings

from .states import ResultMenu
from .text import FINISH_TEXT


def result_menu() -> Window:
    return Window(
        Const(FINISH_TEXT),
        Column(
            Url(Const("Открыть статью"), url=Const(settings.ARTICLE_URL)),
            Url(Const("Подписаться на канал"), id="subscribe_channel", url=Const(settings.CHANNEL_URL)),
        ),
        state=ResultMenu.select_result_menu,
    )
