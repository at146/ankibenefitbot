from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Any

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart, ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from aiohttp import web
from aiohttp.web_app import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.core.config import settings
from bot.dialogs import include_dialogs, start
from bot.dialogs.menu.error import on_unknown_intent, on_unknown_state
from bot.utils import logging

if TYPE_CHECKING:
    from logging import Logger


async def lifespan(app: Application) -> AsyncGenerator[None, Any]:
    dispatcher: Dispatcher = app["main_dp"]
    bot: Bot = app["bot"]
    log: Logger = dispatcher["log"]

    if settings.ENVIRONMENT != "production":
        log.info("Режим: Debug")

    main_bot_url = f"{settings.MAIN_WEBHOOK_ADDRESS}{settings.MAIN_BOT_PATH}"
    url_main = main_bot_url.format(bot_token=settings.BOT_TOKEN)
    await bot.set_webhook(
        url=url_main,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=settings.MAIN_WEBHOOK_SECRET_TOKEN,
    )
    log.info("Set webhook main - %s", url_main)
    log.info("Configured webhook")

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()

    dispatcher["scheduler"] = scheduler

    info_bot = await bot.get_me()
    log.info("<Бот @%s запущен>", info_bot.username)

    yield

    log.info("Stopping bot")
    # Close aiohttp session
    await bot.session.close()
    log.info("Stopped bot")


def main() -> None:
    logger = logging.setup_logger()
    session = AiohttpSession()
    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    storage = MemoryStorage()
    main_bot_dispatcher = Dispatcher(storage=storage, log=logger)
    main_bot_dispatcher.message.register(start.bot_start, CommandStart())
    # dp.errors.register(error_handler.errors_handler)
    main_bot_dispatcher.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    main_bot_dispatcher.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(UnknownState),
    )
    include_dialogs(main_bot_dispatcher)
    setup_dialogs(main_bot_dispatcher)

    app = web.Application()
    # Не получается - Data Sharing aka No Singletons Please
    # https://docs.aiohttp.org/en/stable/web_advanced.html#data-sharing-aka-no-singletons-please
    app["bot"] = bot
    app["main_dp"] = main_bot_dispatcher
    app.cleanup_ctx.append(lifespan)
    SimpleRequestHandler(dispatcher=main_bot_dispatcher, bot=bot).register(app, path=settings.MAIN_BOT_PATH)
    web.run_app(
        app,
        host=settings.MAIN_WEBHOOK_LISTENING_HOST,
        port=settings.MAIN_WEBHOOK_LISTENING_PORT,
    )


if __name__ == "__main__":
    main()
