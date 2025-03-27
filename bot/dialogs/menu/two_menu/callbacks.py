import datetime

from aiogram.types import Chat, FSInputFile, User
from aiogram_dialog import DialogManager
from apscheduler.triggers.date import DateTrigger

from bot.core.config import settings
from bot.init import bot, scheduler

from .keyboards import article_kb, channel_kb
from .text import LAST_MESSAGE_TEXT, TEXT_AFTER_2_HOURS, TEXT_AFTER_10_MIN, TEXT_AFTER_21_HOURS


async def on_start(
    data: dict[str, str],
    manager: DialogManager,
) -> None:
    if settings.ENVIRONMENT == "production":
        trigger = DateTrigger(
            run_date=datetime.datetime.now() + datetime.timedelta(minutes=10), timezone="Europe/Moscow"
        )
    else:
        trigger = DateTrigger(
            run_date=datetime.datetime.now() + datetime.timedelta(seconds=10), timezone="Europe/Moscow"
        )
    event_from_user: User = manager.middleware_data["event_from_user"]
    event_chat: Chat = manager.middleware_data["event_chat"]
    scheduler.add_job(
        change_message_after_10_minutes,
        trigger=trigger,
        args=[
            event_chat.id,
            event_from_user.id,
            data["message_id"],
            event_from_user.first_name,
        ],
        name="after_5_minutes",
    )


async def change_message_after_10_minutes(chat_id: int, user_id: int, message_id: int, first_name: str) -> None:
    last_message = await bot.send_message(
        chat_id=chat_id,
        text=TEXT_AFTER_10_MIN.format(first_name=first_name),
        reply_markup=article_kb(user_id, "Получить статью сейчас"),
    )
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    if settings.ENVIRONMENT == "production":
        trigger = DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(hours=2), timezone="Europe/Moscow")
    else:
        trigger = DateTrigger(
            run_date=datetime.datetime.now() + datetime.timedelta(seconds=10), timezone="Europe/Moscow"
        )
    scheduler.add_job(
        change_message_after_2_hours,
        trigger=trigger,
        args=[
            last_message.chat.id,
            user_id,
            last_message.message_id,
        ],
        name="after_2_hours",
    )


async def change_message_after_2_hours(chat_id: int, user_id: int, message_id: int) -> None:
    last_message = await bot.send_photo(
        chat_id=chat_id,
        photo=FSInputFile("bot/images/IMG_4575.PNG"),
        caption=TEXT_AFTER_2_HOURS,
        reply_markup=channel_kb(user_id, "Подписаться"),
    )
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    if settings.ENVIRONMENT == "production":
        trigger = DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(hours=21), timezone="Europe/Moscow")
    else:
        trigger = DateTrigger(
            run_date=datetime.datetime.now() + datetime.timedelta(seconds=10), timezone="Europe/Moscow"
        )
    scheduler.add_job(
        change_message_after_21_hours,
        trigger=trigger,
        args=[
            last_message.chat.id,
            user_id,
            last_message.message_id,
        ],
        name="after_21_hours",
    )


async def change_message_after_21_hours(chat_id: int, user_id: int, message_id: int) -> None:
    last_message = await bot.send_message(
        chat_id=chat_id,
        text=TEXT_AFTER_21_HOURS,
        reply_markup=article_kb(user_id, "Получить статью сейчас"),
    )
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    if settings.ENVIRONMENT == "production":
        trigger = DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(hours=1), timezone="Europe/Moscow")
    else:
        trigger = DateTrigger(
            run_date=datetime.datetime.now() + datetime.timedelta(seconds=10), timezone="Europe/Moscow"
        )
    scheduler.add_job(
        delete_message,
        trigger=trigger,
        args=[
            last_message.chat.id,
            last_message.message_id,
        ],
        name="delete_message",
    )


async def delete_message(chat_id: int, message_id: int) -> None:
    await bot.send_message(chat_id=chat_id, text=LAST_MESSAGE_TEXT)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
