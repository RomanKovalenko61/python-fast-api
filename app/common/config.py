from typing import Annotated

from fastapi import Depends
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    name: str


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

    # Kafka
    kafka_bootstrap_servers: list[str] = ["localhost:9092"]
    kafka_consumer_group: str = "fastapi-app"
    kafka_auto_offset_reset: str = "earliest"  # "earliest" или "latest"

    # Topics
    orders_topic: str = "orders"
    notifications_topic: str = "notifications"

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.database_url)

    @property
    def app(self) -> AppSettings:
        return AppSettings(name=self.service_name)


def get_settings() -> Settings:
    return Settings()


SettingsDeps = Annotated[
    Settings,
    Depends(get_settings),
]
