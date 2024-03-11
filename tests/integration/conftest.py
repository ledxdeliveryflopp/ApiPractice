import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def AuthClient(AppSetUp):
    async with AsyncClient(app=AppSetUp, base_url="http://localhost:7000/authorization/") as client:
        yield client
