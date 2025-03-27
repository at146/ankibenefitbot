from typing import Any

from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.crud import users_db, users_lidmagnit_db


async def get_data_spam_menu(db_session: async_sessionmaker[AsyncSession], **kwargs: dict[str, Any]) -> dict[str, str]:
    users_lidmagnit = await users_lidmagnit_db.get_count(db_session)
    users = await users_db.get_count(db_session)
    if users_lidmagnit is None:
        raise Exception("Не удалось получить количество пользователей из базы данных")
    if users is None:
        raise Exception("Не удалось получить количество пользователей из базы данных")
    return {
        "all_users": str(users_lidmagnit + users),
    }


async def get_data_result_spam_menu(dialog_manager: DialogManager, **kwargs: dict[str, Any]) -> dict[str, str]:
    return {"result_spam_text": dialog_manager.dialog_data["result_spam_text"]}
