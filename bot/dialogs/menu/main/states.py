from aiogram.fsm.state import State, StatesGroup


class BotMenu(StatesGroup):
    select_main_menu = State()
