import asyncio

from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeChat,
)

from bot.core.config import settings


async def set_bot_commands(bot: Bot) -> bool:
    # для админов только bot command
    admin_commands = [BotCommand(command="admin", description="Админ панель")]
    async with asyncio.TaskGroup() as task_group:
        tasks = [
            task_group.create_task(bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=chat_id)))
            for chat_id in settings.BOT_ADMINS_IDS
        ]
    return all(task.result() for task in tasks)
