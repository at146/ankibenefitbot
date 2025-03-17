from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const

from .callbacks import start_questioning_clicked
from .keyboards import main_kb
from .states import BotMenu
from .text import START_TEXT


def main_menu() -> Window:
    return Window(
        Const(START_TEXT),
        main_kb(start_questioning_clicked),
        state=BotMenu.select_main_menu,
    )
