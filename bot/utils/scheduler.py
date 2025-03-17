from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.core.config import settings


def setup_scheduler() -> AsyncIOScheduler:
    redis_job_store = RedisJobStore(
        db=int(settings.REDIS_DB),
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        username=settings.REDIS_USER,
        socket_timeout=5,
    )

    jobstores = {"default": redis_job_store}
    return AsyncIOScheduler(timezone="Europe/Moscow", jobstores=jobstores)
