import logging
import os
from logging.config import dictConfig

from bot.core.config import settings

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "class": "logging.Formatter",
            "datefmt": "%d-%m-%Y %H:%M:%S",
            "format": "%(asctime)s (%(name)s:%(filename)s:%(lineno)d) %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "basic",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "basic",
            "filename": "logs/log.log",
            "when": "midnight",
            "backupCount": 31,
            "encoding": "utf-8",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "level": "WARNING",
            "formatter": "basic",
            "filename": "logs/error_log.log",
            "mode": "a",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "aiogram_dialog": {
            "level": "DEBUG",
        },
        "asyncio": {
            "level": "DEBUG",
        },
        "apscheduler": {
            "level": "DEBUG",
        },
        "tzlocal": {
            "level": "INFO",
        },
        "urllib3": {
            "level": "INFO",
        },
        "": {
            "handlers": ["file", "error_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


def setup_logger() -> logging.Logger:
    if settings.ENVIRONMENT == "production":
        LOGGER_CONFIG["loggers"][""]["handlers"] = ["file", "error_file"]  # type: ignore
        LOGGER_CONFIG["loggers"]["aiogram_dialog"]["level"] = "INFO"  # type: ignore
        LOGGER_CONFIG["loggers"]["asyncio"]["level"] = "INFO"  # type: ignore
        LOGGER_CONFIG["loggers"]["apscheduler"]["level"] = "INFO"  # type: ignore
        LOGGER_CONFIG["loggers"]["urllib3"]["level"] = "INFO"  # type: ignore

    if not os.path.exists("logs"):
        os.mkdir("logs")
    dictConfig(LOGGER_CONFIG)
    return logging.getLogger(__name__)
