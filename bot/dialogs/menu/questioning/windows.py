from aiogram.fsm.state import State
from aiogram.utils.text_decorations import html_decoration
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Column, Group, Select
from aiogram_dialog.widgets.text import Const, Format

from .callbacks import question_clicked
from .states import QuestioningMenu
from .text import DICT_QUESTIONS, LAST_QUESTION


def choose_state(number_question: str) -> State:
    state_name = f"select_{number_question}_menu"
    state = getattr(QuestioningMenu, state_name, None)
    if state is None:
        raise ValueError(f"Unknown number question: {number_question}")
    return state  # type: ignore[no-any-return]


def generate_menu() -> list[Window]:
    list_of_windows = []
    for number_question, value in DICT_QUESTIONS.items():
        count_selects = len(value["variants"])
        if count_selects == 4:
            selects = ["1", "2", "3", "4"]
        elif count_selects == 6:
            selects = ["1", "2", "3", "4", "5", "6"]
        else:
            raise ValueError(f"Unknown count of selects: {count_selects}")

        if not isinstance(value["question"], str):
            raise ValueError(f"Question is not string: {value['question']}")

        text = ""
        if "before_additional_text" in value and isinstance(value["before_additional_text"], str):
            text += value["before_additional_text"]
        text += html_decoration.bold(f"{number_question}/{len(DICT_QUESTIONS)}. {value['question']}")
        text += "\n\n"

        for index, variant in enumerate(value["variants"], 1):
            text += f"[{index}] — {variant}\n"

        list_of_windows.append(
            Window(
                Const(text),
                Group(
                    Select(
                        Format("{item}"),
                        items=selects,
                        item_id_getter=lambda x: x,
                        id=number_question,
                        on_click=question_clicked,
                    ),
                    width=2,
                ),
                state=choose_state(number_question),
            )
        )

    list_of_windows.append(
        Window(
            Const(LAST_QUESTION["question"]),  # type: ignore
            Column(
                Select(
                    Format("{item}"),
                    items=LAST_QUESTION["variants"],
                    item_id_getter=lambda x: LAST_QUESTION["variants"].index(x) + 1,
                    id="last",
                    on_click=question_clicked,
                ),
            ),
            state=QuestioningMenu.select_last_menu,
        )
    )

    return list_of_windows
