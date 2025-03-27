from aiogram import Router
from aiogram.filters import Command, CommandStart

from bot.handlers import chat_join_request
from bot.handlers.users import admin, start


def prepare_router() -> Router:
    router = Router(name="router")
    # start
    router.message.register(start.bot_start, CommandStart())
    router.chat_join_request.register(chat_join_request.bot_chat_join_request)

    # admin_menu
    router.message.register(admin.command_admin, Command(commands=["admin"]))
    return router
