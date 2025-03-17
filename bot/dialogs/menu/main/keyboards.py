from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const


def main_kb(on_click) -> Button:  # type: ignore
    return Button(
        Const("Заполнить"),
        id="go",  # id is used to detect which button is clicked
        on_click=on_click,
    )
