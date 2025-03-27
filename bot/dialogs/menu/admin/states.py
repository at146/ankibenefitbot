from aiogram.fsm.state import State, StatesGroup


class AdminMenu(StatesGroup):
    main_menu = State()
    spam_menu = State()
    text = State()
    result = State()
