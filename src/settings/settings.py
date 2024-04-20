from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    """Настройки jwt токенов"""
    jwt_secret: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SqlSettings(BaseSettings):
    """Настройки для БД"""
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def db_full_url(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")


class VaultSettings(BaseSettings):
    """Настройки для vault"""
    vault_url: str
    vault_token_app: str
    vault_mount: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class BrokerSettings(BaseSettings):
    """Настройки для RabbitMQ"""
    broker_username: str
    broker_password: str
    broker_host: str
    broker_port: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def broker_full_url(self) -> str:
        return (f"amqp://{self.broker_username}:{self.broker_password}@"
                f"{self.broker_host}:{self.broker_port}")


class UrlSettings(BaseSettings):
    """Настройки url для тестов"""
    auth_url: str
    register_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Все настройки"""
    jwt_settings: JwtSettings
    sql_settings: SqlSettings
    url_settings: UrlSettings
    vault_settings: VaultSettings
    broker_settings: BrokerSettings


@lru_cache()
def init_settings() -> object:
    """Инициализация настроек"""
    all_settings = Settings(jwt_settings=JwtSettings(), sql_settings=SqlSettings(),
                            url_settings=UrlSettings(),
                            vault_settings=VaultSettings(), broker_settings=BrokerSettings())
    return all_settings


settings = init_settings()

