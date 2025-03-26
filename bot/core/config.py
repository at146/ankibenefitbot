from typing import Literal

from pydantic import (
    PostgresDsn,
    RedisDsn,
    computed_field,
)
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    # .env
    ENVIRONMENT: Literal["local", "production"] = "local"
    BOT_TOKEN: str

    MAIN_WEBHOOK_ADDRESS: str
    MAIN_BOT_PATH: str
    MAIN_WEBHOOK_SECRET_TOKEN: str
    MAIN_WEBHOOK_LISTENING_HOST: str
    MAIN_WEBHOOK_LISTENING_PORT: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    ARTICLE_REDIRECT_URL: str
    CHANNEL_REDIRECT_URL: str

    USE_REDIS: bool
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_URI(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USER,
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=self.REDIS_DB,
        )

    GOOGLE_SHEET_TABLE_ID: str
    GOOGLE_PATH_CREDITS: str
    GOOGLE_SHEET_MINUTE_CHECK_TABLE: int
    # Если добавляются в этот канал, то добавляется в базу
    GOOGLE_SHEET_TELEGRAM_CHANNEL_ID: int

    ARTICLE_URL: str
    CHANNEL_URL: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            dotenv_settings,
        )


settings = Settings()  # type: ignore
