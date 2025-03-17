from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.config import settings


def article_kb(user_id: int, text: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=text, url=settings.ARTICLE_REDIRECT_URL.format(user_id=user_id))
    builder.button(text="Получить статью сейчас", url=settings.ARTICLE_REDIRECT_URL.format(user_id=user_id))
    return builder.as_markup()
