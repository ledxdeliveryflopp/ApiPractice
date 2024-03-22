from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    """Настройки jwt токенов"""
    jwt_secret: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SqlSettings(BaseSettings):
    """Настройки для БД"""
    sql_user: str
    sql_password: str
    sql_host: str
    sql_port: str
    sql_name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def db_full_url(self) -> str:
        return (f"postgresql+asyncpg://{self.sql_user}:{self.sql_password}@"
                f"{self.sql_host}:{self.sql_port}/{self.sql_name}")


class UrlSettings(BaseSettings):
    """Настройки url для тестов"""
    auth_url: str
    register_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


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


class Settings(BaseSettings):
    """Все настройки"""
    jwt_settings: JwtSettings
    sql_settings: SqlSettings
    url_settings: UrlSettings
    vault_settings: VaultSettings
    broker_settings: BrokerSettings


@lru_cache()
def init_settings():
    """Инициализация настроек"""
    all_settings = Settings(jwt_settings=JwtSettings(), sql_settings=SqlSettings(),
                            url_settings=UrlSettings(),
                            vault_settings=VaultSettings(), broker_settings=BrokerSettings())
    return all_settings


settings = init_settings()

