from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Checkbox, Column, Start
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.menu.admin.callbacks import admin_text_spam

from .getters import get_data_result_spam_menu, get_data_spam_menu
from .states import AdminMenu


def main_menu() -> Window:
    return Window(
        Const("<b>Панель администратора</b>"),
        Start(Const("💬 Рассылка"), id="spam", state=AdminMenu.spam_menu),
        state=AdminMenu.main_menu,
    )


def spam_menu() -> Window:
    mess_text = (
        "Рассылка будет отправлена <b>{all_users} чел.</b>\n"
        "Вы получите отчет после ее завершения.\n\n"
        "Выберите вид рассылки:"
    )

    return Window(
        Format(mess_text),
        Column(
            # Start(Const("Рассылка с кнопкой"), id="buttons", state=AdminMenu.spam_menu),
            Start(Const("Рассылка без кнопки"), id="text", state=AdminMenu.text),
        ),
        Cancel(text=Const("Отмена")),
        state=AdminMenu.spam_menu,
        getter=get_data_spam_menu,
    )


def text_spam_menu() -> Window:
    mess_text = (
        "Пришлите <b>текст, видео, анимацию или фотографию (с подписью или без).</b> "
        "Данные отправятся пользователям бота. "
        "(Функция не поддерживает: документы, "
        "отправку нескольких фотографий в одном сообщении).\n\n"
    )

    return Window(
        Const(mess_text),
        MessageInput(
            func=admin_text_spam,
            content_types=[ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION],
        ),
        Checkbox(
            checked_text=Const("❌ Превью ссылки"),
            unchecked_text=Const("✅ Превью ссылки"),
            id="disable_web_page_preview",
        ),
        Cancel(Const("Отмена")),
        state=AdminMenu.text,
    )


def result_spam_menu() -> Window:
    return Window(
        Format("{result_spam_text}"),
        state=AdminMenu.result,
        getter=get_data_result_spam_menu,
    )
