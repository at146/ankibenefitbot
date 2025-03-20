from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.data import MiddlewareData
from aiogram.types import Message, TelegramObject


class EmptyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        return await handler(event, data)


class MyMiddlewareData(MiddlewareData, total=False):
    my_custom_value: int


class MyMessageMiddleware(BaseMiddleware):
    async def __call__(  # type: ignore
        self,
        handler: Callable[[Message, MyMiddlewareData], Awaitable[Any]],
        event: Message,
        data: MyMiddlewareData,
    ) -> Any:
        bot = data["bot"]  # <-- IDE will show you that data has `bot` key and its type is `Bot` # type: ignore

        data["my_custom_value"] = (
            bot.id * 42
        )  # <-- IDE will show you that you can set `my_custom_value` key with int value and warn you if you try to set it with other type  # noqa: E501
        return await handler(event, data)
