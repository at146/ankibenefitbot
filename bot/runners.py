from logging import Logger

from aiogram import Bot, Dispatcher, loggers
from aiogram.webhook import aiohttp_server as server
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot.api.google_sheets.anki_sheet import AnkiSheet
from bot.core.config import Settings, settings
from bot.db.session import db_session
from bot.init import scheduler
from bot.utils.bot_commands import set_bot_commands


async def polling_startup(dispatcher: Dispatcher, bot: Bot, log: Logger) -> None:
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

    # TODO: как удалить админа бота
    if await set_bot_commands(bot):
        log.info("Set bot commands")
    else:
        log.error("Error set bot commands")

    await bot.delete_webhook(drop_pending_updates=settings.DROP_PENDING_UPDATES)
    if settings.DROP_PENDING_UPDATES:
        loggers.dispatcher.info("Updates skipped successfully")


async def polling_shutdown(dispatcher: Dispatcher) -> None:
    scheduler: AsyncIOScheduler = dispatcher["scheduler"]
    scheduler.shutdown()


async def webhook_startup(dispatcher: Dispatcher, bot: Bot, log: Logger) -> None:
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
    # TODO: как удалить админа бота
    if await set_bot_commands(bot):
        log.info("Set bot commands")
    else:
        log.error("Error set bot commands")
    main_bot_url = f"{settings.MAIN_WEBHOOK_ADDRESS}{settings.MAIN_BOT_PATH}"
    url_main = main_bot_url.format(bot_token=settings.BOT_TOKEN)
    used_update_types = dispatcher.resolve_used_update_types()
    log.info("Used update types: %s", used_update_types)
    log.info("Configuring webhook")
    if await bot.set_webhook(
        url=url_main,
        allowed_updates=used_update_types,
        secret_token=settings.MAIN_WEBHOOK_SECRET_TOKEN,
    ):
        log.info("Set webhook main - %s", url_main)
        log.info("Configured webhook")

        info_bot = await bot.get_me()
        log.info("<Бот @%s запущен>", info_bot.username)
    else:
        loggers.webhook.error("Failed to set main bot webhook on url '%s'", url_main)


async def webhook_shutdown(bot: Bot, log: Logger) -> None:
    # log.info("Removing webhook")
    # await bot.delete_webhook()
    # log.info("Webhook removed")
    log.info("Shutting down scheduler")
    scheduler.shutdown()
    log.info("Scheduler shutdown")
    if not settings.RESET_WEBHOOK:
        return
    if await bot.delete_webhook():
        loggers.webhook.info("Dropped main bot webhook.")
    else:
        loggers.webhook.error("Failed to drop main bot webhook.")
    log.info("Stopping bot")
    # Close aiohttp session
    await bot.session.close()
    log.info("Stopped bot")


def run_polling(dispatcher: Dispatcher, bot: Bot, log: Logger) -> None:
    dispatcher.startup.register(polling_startup)
    dispatcher.shutdown.register(polling_shutdown)
    used_update_types = dispatcher.resolve_used_update_types()
    log.info("Used update types: %s", used_update_types)
    return dispatcher.run_polling(
        bot,
        allowed_updates=used_update_types,
    )


def run_webhook(dispatcher: Dispatcher, bot: Bot, settings: Settings) -> None:
    app: web.Application = web.Application()
    server.SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        # secret_token=config.telegram.webhook_secret.get_secret_value(),
    ).register(app, path=settings.MAIN_BOT_PATH)

    server.setup_application(app, dispatcher, bot=bot)
    app.update(**dispatcher.workflow_data, bot=bot)
    dispatcher.startup.register(webhook_startup)
    dispatcher.shutdown.register(webhook_shutdown)
    return web.run_app(
        app=app,
        host=settings.MAIN_WEBHOOK_LISTENING_HOST,
        port=settings.MAIN_WEBHOOK_LISTENING_PORT,
    )
