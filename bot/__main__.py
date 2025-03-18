from collections.abc import AsyncGenerator
from typing import Any

from aiogram import Dispatcher
from aiogram.filters import CommandStart, ExceptionTypeFilter
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from aiohttp import web
from aiohttp.web_app import Application
from apscheduler.triggers.interval import IntervalTrigger

from bot.api.google_sheets.anki_sheet import AnkiSheet
from bot.core.config import settings
from bot.db.session import db_session
from bot.dialogs import include_dialogs, start
from bot.dialogs.menu.error import on_unknown_intent, on_unknown_state
from bot.init import bot, log, scheduler


async def lifespan(app: Application) -> AsyncGenerator[None, Any]:
    dispatcher: Dispatcher = app["main_dp"]

    # Создание Engine для db
    dispatcher["db_session"] = db_session

    anki_sheet = AnkiSheet(path_credits=settings.GOOGLE_PATH_CREDITS)
    await anki_sheet.init_table()
    scheduler.add_job(
        anki_sheet.update_table,
        trigger=IntervalTrigger(minutes=settings.GOOGLE_SHEET_MINUTE_CHECK_TABLE, timezone="Europe/Moscow"),
        name="change_google_table",
        id="change_google_table",
        replace_existing=True,
    )

    scheduler.start()
    dispatcher["scheduler"] = scheduler

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

    info_bot = await bot.get_me()
    log.info("<Бот @%s запущен>", info_bot.username)

    yield

    # log.info("Removing webhook")
    # await bot.delete_webhook()
    # log.info("Webhook removed")
    log.info("Shutting down scheduler")
    scheduler.shutdown()
    log.info("Scheduler shutdown")
    log.info("Stopping bot")
    # Close aiohttp session
    await bot.session.close()
    log.info("Stopped bot")


def main() -> None:
    if settings.USE_REDIS:
        storage = RedisStorage.from_url(
            settings.REDIS_URI.unicode_string(), key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True)
        )
    else:
        storage = MemoryStorage()  # type: ignore[assignment]

    main_bot_dispatcher = Dispatcher(storage=storage, log=log)
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
