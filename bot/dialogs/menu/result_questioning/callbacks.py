import datetime

from aiogram_dialog import DialogManager
from apscheduler.triggers.date import DateTrigger

from bot.core.config import settings
from bot.crud import users_db
from bot.db.session import db_session
from bot.init import bot, scheduler

from .keyboards import article_kb
from .text import LAST_MESSAGE_TEXT, TEXT_AFTER_23_HOURS, get_after_5_minutes_text


async def on_start(
    data: dict[str, str],
    manager: DialogManager,
) -> None:
    if settings.ENVIRONMENT == "production":
        trigger = DateTrigger(
            run_date=datetime.datetime.now() + datetime.timedelta(minutes=5), timezone="Europe/Moscow"
        )
    else:
        trigger = DateTrigger(
            run_date=datetime.datetime.now() + datetime.timedelta(seconds=10), timezone="Europe/Moscow"
        )

    scheduler.add_job(
        change_message_after_5_minutes,
        trigger=trigger,
        args=[
            data["chat_id"],
            data["message_id"],
            data["first_name"],
        ],
        name="after_5_minutes",
    )


async def change_message_after_5_minutes(chat_id: int, message_id: int, first_name: str) -> None:
    user_db = await users_db.get_user_by_user_id(chat_id, db_session)

    if user_db is None:
        raise ValueError(f"User not found chat_id - {chat_id}")

    if user_db.is_clicked_article is False:
        last_message = await bot.send_message(
            chat_id=chat_id,
            text=get_after_5_minutes_text(),
            reply_markup=article_kb(chat_id, "Читать статью"),
        )
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        if settings.ENVIRONMENT == "production":
            trigger = DateTrigger(
                run_date=datetime.datetime.now() + datetime.timedelta(hours=23), timezone="Europe/Moscow"
            )
        else:
            trigger = DateTrigger(
                run_date=datetime.datetime.now() + datetime.timedelta(seconds=10), timezone="Europe/Moscow"
            )
        scheduler.add_job(
            change_message_after_23_hours,
            trigger=trigger,
            args=[
                last_message.chat.id,
                last_message.message_id,
            ],
        )


async def change_message_after_23_hours(chat_id: int, message_id: int) -> None:
    user_db = await users_db.get_user_by_user_id(chat_id, db_session)
    if user_db is None:
        raise ValueError(f"User not found chat_id - {chat_id}")
    if user_db.is_clicked_article is False:
        last_message = await bot.send_message(
            chat_id=chat_id,
            text=TEXT_AFTER_23_HOURS,
            reply_markup=article_kb(chat_id, "Забрать статью"),
        )
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        if settings.ENVIRONMENT == "production":
            trigger = DateTrigger(
                run_date=datetime.datetime.now() + datetime.timedelta(hours=1), timezone="Europe/Moscow"
            )
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
        )


async def delete_message(chat_id: int, message_id: int) -> None:
    await bot.send_message(chat_id=chat_id, text=LAST_MESSAGE_TEXT)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
