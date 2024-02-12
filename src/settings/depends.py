from src.settings.db import async_session


async def get_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
