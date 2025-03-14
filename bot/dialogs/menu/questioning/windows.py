from aiogram.fsm.state import State
from aiogram.utils.text_decorations import html_decoration
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Select
from aiogram_dialog.widgets.text import Const, Format

from .callbacks import question_clicked
from .states import QuestioningMenu
from .text import DICT_QUESTIONS


def choose_state(number_question: str) -> State:  # noqa: C901
    if number_question == "1":
        return QuestioningMenu.select_1_menu
    if number_question == "2":
        return QuestioningMenu.select_2_menu
    if number_question == "3":
        return QuestioningMenu.select_3_menu
    if number_question == "4":
        return QuestioningMenu.select_4_menu
    if number_question == "5":
        return QuestioningMenu.select_5_menu
    if number_question == "6":
        return QuestioningMenu.select_6_menu
    if number_question == "7":
        return QuestioningMenu.select_7_menu
    if number_question == "8":
        return QuestioningMenu.select_8_menu
    if number_question == "9":
        return QuestioningMenu.select_9_menu
    if number_question == "10":
        return QuestioningMenu.select_10_menu
    if number_question == "11":
        return QuestioningMenu.select_11_menu
    if number_question == "12":
        return QuestioningMenu.select_12_menu
    if number_question == "13":
        return QuestioningMenu.select_13_menu
    if number_question == "14":
        return QuestioningMenu.select_14_menu
    if number_question == "15":
        return QuestioningMenu.select_15_menu
    if number_question == "16":
        return QuestioningMenu.select_16_menu
    if number_question == "17":
        return QuestioningMenu.select_17_menu
    if number_question == "18":
        return QuestioningMenu.select_18_menu
    if number_question == "19":
        return QuestioningMenu.select_19_menu
    raise ValueError(f"Unknown number question: {number_question}")


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

        # TODO: Убрать это и возможно разделить переменные вопроса и вариантов ответа
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
    return list_of_windows
