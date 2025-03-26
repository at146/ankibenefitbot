from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .callbacks import start_two_menu_clicked
from .states import BotMenu
from .text import MAIN_MENU_TEXT


def main_menu() -> Window:
    return Window(
        Const(MAIN_MENU_TEXT),
        Button(
            Const("Забрать статью"),
            id="go",
            on_click=start_two_menu_clicked,
        ),
        state=BotMenu.select_main_menu,
    )
