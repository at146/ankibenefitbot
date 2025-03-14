from sqlalchemy.ext.asyncio import create_async_engine

from .config import settings

async_engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,  # log all SQL queries
    connect_args={"server_settings": {"application_name": settings.ENVIRONMENT}},
)
