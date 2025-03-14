from typing import Literal

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
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BOT_TOKEN: str

    MAIN_WEBHOOK_ADDRESS: str
    MAIN_BOT_PATH: str
    MAIN_WEBHOOK_SECRET_TOKEN: str
    MAIN_WEBHOOK_LISTENING_HOST: str
    MAIN_WEBHOOK_LISTENING_PORT: int

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (dotenv_settings,)


settings = Settings()  # type: ignore
