from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def article_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить статью сейчас", url="https://127.0.0.1")
    return builder.as_markup()


def article_last_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Забрать статью", url="https://127.0.0.1")
    return builder.as_markup()
