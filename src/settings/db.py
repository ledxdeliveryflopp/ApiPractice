from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.settings.settings import settings

engine = create_async_engine(
    url=f"postgresql+asyncpg://{settings.sql_settings.sql_user}:"
        f"{settings.sql_settings.sql_password}@{settings.sql_settings.sql_host}:"
        f"{settings.sql_settings.sql_port}/{settings.sql_settings.sql_name}",
    echo=False
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


Base = declarative_base()
