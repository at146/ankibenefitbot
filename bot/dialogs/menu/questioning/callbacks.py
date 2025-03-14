from typing import Any

from aiogram.types import User
from aiogram_dialog import ChatEvent, DialogManager

from bot.dialogs.menu.result_questioning.states import ResultMenu

from .text import DICT_QUESTIONS


async def question_clicked(
    callback: ChatEvent,
    select: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    # select.widget_id - номер вопроса
    if select.widget_id is None:
        raise ValueError("Select Widget ID is None")

    manager.dialog_data[select.widget_id] = DICT_QUESTIONS[select.widget_id]["variants"][int(item_id) - 1]

    # TODO: костыль
    # if select.widget_id == "19":
    if select.widget_id == "3":
        # await manager.done()
        event_from_user: User = manager.middleware_data["event_from_user"]
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


# async def def_on_close(
#     callback: ChatEvent,
#     manager: DialogManager,
# ):
#     pass

# async def on_start(
#     callback: ChatEvent,
#     manager: DialogManager,
# ):
#     pass


# async def process_result(
#     start_data: Data,
#     result: Any,
#     manager: DialogManager,
# ):
#     if result:
#         manager.dialog_data["name"] = result["name"]
