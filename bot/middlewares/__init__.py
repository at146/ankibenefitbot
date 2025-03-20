from aiogram import Dispatcher

from bot.middlewares.middleware import EmptyMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(EmptyMiddleware())
