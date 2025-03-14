from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.dialogs.menu.questioning.states import QuestioningMenu


async def start_questioning_clicked(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    # await manager.done()
    await manager.start(QuestioningMenu.select_1_menu)
