import datetime

from aiogram_dialog import DialogManager
from apscheduler.triggers.date import DateTrigger

from bot.init import bot, scheduler

from .keyboards import article_kb, article_last_kb
from .text import TEXT_AFTER_23_HOURS, get_after_5_minutes_text


async def on_start(
    data: dict[str, str],
    manager: DialogManager,
) -> None:
    # TODO: для локальной разработки меньше поставить тригер
    trigger = DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(minutes=5))
    scheduler.add_job(
        change_message_after_5_minutes,
        trigger=trigger,
        args=[
            data["chat_id"],
            data["message_id"],
            data["first_name"],
        ],
    )


async def change_message_after_5_minutes(chat_id: int, message_id: int, first_name: str) -> None:
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    last_message = await bot.send_message(
        chat_id=chat_id,
        text=get_after_5_minutes_text(first_name),
        reply_markup=article_kb(),
    )
    # TODO: для локальной разработки меньше поставить тригер
    trigger = DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(hours=23))
    scheduler.add_job(
        change_message_after_23_hours,
        trigger=trigger,
        args=[
            last_message.chat.id,
            last_message.message_id,
        ],
    )


async def change_message_after_23_hours(chat_id: int, message_id: int) -> None:
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_message(
        chat_id=chat_id,
        text=TEXT_AFTER_23_HOURS,
        reply_markup=article_last_kb(),
    )
