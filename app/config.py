import os
import redis
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Корневая директория проекта


    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env-prod", extra="allow")

    def get_bd_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_redis_cache_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    def get_redis_broker_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"

    def get_redis_back_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/3"


settings = Settings()

redis_client = redis.from_url(settings.get_redis_cache_url())
redis_email_client = redis.from_url(settings.get_redis_back_url())
