import os

from enum import Enum
from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, RedisDsn

load_dotenv()


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    DEBUG: int = os.environ.get('DEBUG')
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = os.environ.get('ENVIRONMENT')
    POSTGRES_URL: PostgresDsn = (
        os.environ.get('POSTGRES_URL')
    )
    MONGO_URI = os.environ.get('MONGO_URI')
    REDIS_URL: RedisDsn = os.environ.get('REDIS_URL')
    RELEASE_VERSION: str = "0.1"
    SHOW_SQL_ALCHEMY_QUERIES: int = 0
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    JWT_ALGORITHM: str = os.environ.get('JWT_ALGORITHM')
    JWT_EXPIRE_MINUTES: int = 60 * 24
    CELERY_BROKER_URL: str = os.environ.get('CELERY_BROKER_URL')
    CELERY_BACKEND_URL: str = os.environ.get('CELERY_BACKEND_URL')


config: Config = Config()