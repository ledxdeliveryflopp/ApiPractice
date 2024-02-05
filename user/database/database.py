import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

database_url = os.getenv("DATABASE_URL")

engine = create_async_engine(
    database_url, _class=AsyncSession, echo=True
)

Base = declarative_base()
