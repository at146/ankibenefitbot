from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.core.config import settings


def article_kb(user_id: int, text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, url=settings.ARTICLE_REDIRECT_URL.format(user_id=user_id))]]
    )


def channel_kb(user_id: int, text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, url=settings.CHANNEL_REDIRECT_URL.format(user_id=user_id))]]
    )
