from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from bot.core.config import settings


def setup_db_session() -> async_sessionmaker[AsyncSession]:
    async_engine: AsyncEngine = create_async_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        echo=False,  # log all SQL queries
        connect_args={"server_settings": {"application_name": settings.ENVIRONMENT}},
    )
    return async_sessionmaker(bind=async_engine, expire_on_commit=False, autoflush=False)
