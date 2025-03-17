from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from bot.core.config import settings
from bot.utils import logging
from bot.utils.scheduler import setup_scheduler

log = logging.setup_logger()
session = AiohttpSession()
bot = Bot(
    token=settings.BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode="HTML"),
)
scheduler = setup_scheduler()
