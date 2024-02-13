from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sql_url: str = "postgresql+asyncpg://postgres:postgres@database-1:5432/postgres"
    secret_key: str = "1ca26a466e6327dfd6e51599fd2892e59ba1a2885ab3d9b09f48baaa3ca2251c"
    algorithm: str = "HS256"
    auth_url: str = "http://localhost:7000/authorization"
    register_url: str = "http://localhost:7000/registration"

