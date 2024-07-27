from pathlib import Path
from typing import Optional

from pydantic import Field, PostgresDsn, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from bot.enums.bot_mode import BotMode


class Settings(BaseSettings):
    bot_token: SecretStr = Field(validation_alias="BOT_CONFIG")
    mode: BotMode = Field(validation_alias="BOT_MODE")
    db_url: Optional[PostgresDsn] = Field(validation_alias="DB_URL", default=None)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.joinpath(".env"),
        env_file_encoding="utf-8",
    )

    # noinspection PyNestedDecorators
    @field_validator("db_url")
    @classmethod
    def skip_db_url_validation(cls, value: PostgresDsn, info: ValidationInfo):
        if info.data.get("mode") != BotMode.develop and value is None:
            raise ValueError("BOT_MODE is PRODUCT, but DB_URL is missing!")
        return value
