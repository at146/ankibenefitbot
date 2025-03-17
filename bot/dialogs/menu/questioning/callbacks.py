from typing import Any

from aiogram.types import User
from aiogram_dialog import ChatEvent, DialogManager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.crud.answers_questions_db import insert_answers_questions
from bot.dialogs.menu.result_questioning.states import ResultMenu

from .text import DICT_QUESTIONS, LAST_QUESTION


async def question_clicked(
    callback: ChatEvent,
    select: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    if select.widget_id is None:
        raise ValueError("Select Widget ID is None")

    if select.widget_id == "last":
        manager.dialog_data[select.widget_id] = LAST_QUESTION["variants"][int(item_id) - 1]
    else:
        manager.dialog_data[select.widget_id] = DICT_QUESTIONS[select.widget_id]["variants"][int(item_id) - 1]

    # Вопросы кончились
    if select.widget_id == "last":
        # await manager.done()
        event_from_user: User = manager.middleware_data["event_from_user"]
        db_session: async_sessionmaker[AsyncSession] = manager.middleware_data["db_session"]

        result = {}
        for key, value in manager.dialog_data.items():
            if key == "last":
                result[LAST_QUESTION["question"]] = value
            else:
                result[DICT_QUESTIONS[key]["question"]] = value

        await insert_answers_questions(event_from_user.id, str(result), db_session)
        await manager.start(
            ResultMenu.select_result_menu,
            data={
                "chat_id": event_from_user.id,
                "message_id": callback.message.message_id,  # type: ignore
                "first_name": event_from_user.first_name,
            },
        )
    else:
        await manager.next()
