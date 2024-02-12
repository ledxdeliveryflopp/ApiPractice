from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sql_url: str = "postgresql+asyncpg://postgres:postgres@database-1:5432/postgres"

