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


class Settings(BaseSettings):
    """Все настройки"""
    jwt_settings: JwtSettings
    sql_settings: SqlSettings
    url_settings: UrlSettings
    vault_settings: VaultSettings


@lru_cache()
def init_settings():
    """Инициализация настроек"""
    all_settings = Settings(jwt_settings=JwtSettings(), sql_settings=SqlSettings(),
                            url_settings=UrlSettings(),
                            vault_settings=VaultSettings())
    return all_settings


settings = init_settings()

