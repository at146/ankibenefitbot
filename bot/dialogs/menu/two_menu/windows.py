from typing import Any

from aiogram.types import User
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Column, Url
from aiogram_dialog.widgets.text import Const, Format

from bot.core.config import settings

from .states import TwoMenu
from .text import TWO_MENU_TEXT


async def get_data(event_from_user: User, **kwargs: dict[str, Any]) -> dict[str, str]:
    return {
        "ARTICLE_REDIRECT_URL": settings.ARTICLE_REDIRECT_URL.format(user_id=event_from_user.id),
        "CHANNEL_REDIRECT_URL": settings.CHANNEL_REDIRECT_URL.format(user_id=event_from_user.id),
    }


def two_menu() -> Window:
    return Window(
        Const(TWO_MENU_TEXT),
        Column(
            Url(
                Const("Открыть статью"),
                url=Format("{ARTICLE_REDIRECT_URL}"),
            ),
            Url(
                Const("Подписаться на канал"),
                id="subscribe_channel",
                url=Format("{CHANNEL_REDIRECT_URL}"),
            ),
        ),
        state=TwoMenu.select_two_menu,
        getter=get_data,
    )
