import os

import redis
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

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
    REDIS_PASSWORD: str
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Корневая директория проекта

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", extra="allow")

    def get_bd_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_redis_cache_url(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    def get_redis_broker_url(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/1"

    def get_redis_back_url(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/3"


settings = Settings()

redis_client = redis.from_url(settings.get_redis_cache_url(), decode_responses=True)

