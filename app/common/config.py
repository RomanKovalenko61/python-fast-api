from typing import Annotated

from fastapi import Depends
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    debug: bool = False

    service_name: str = Field(validation_alias="SERVICE_NAME")
    database_url: str = Field(validation_alias="DATABASE_URL")

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.database_url)


def get_settings() -> Settings:
    return Settings()


SettingsDeps = Annotated[
    Settings,
    Depends(get_settings),
]
