from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.dialogs.menu.two_menu.states import TwoMenu


async def start_two_menu_clicked(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    # await manager.done()
    if callback.message:
        await manager.start(TwoMenu.select_two_menu, data={"message_id": callback.message.message_id})
