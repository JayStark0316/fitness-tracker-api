from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    db_url: str
    db_name: str
    aes_key: str


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()