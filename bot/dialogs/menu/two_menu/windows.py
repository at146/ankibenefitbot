from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Column, Url
from aiogram_dialog.widgets.text import Const

from bot.core.config import settings

from .states import TwoMenu
from .text import TWO_MENU_TEXT


def two_menu() -> Window:
    return Window(
        Const(TWO_MENU_TEXT),
        Column(
            Url(
                Const("Открыть статью"),
                url=Const(settings.ARTICLE_URL),
            ),
            Url(
                Const("Подписаться на канал"),
                id="subscribe_channel",
                url=Const(settings.CHANNEL_URL),
            ),
        ),
        state=TwoMenu.select_two_menu,
    )
