import pytest
from httpx import AsyncClient
from src.settings.settings import settings


@pytest.fixture
async def RegisterClient(AppSetUp):
    async with AsyncClient(app=AppSetUp, base_url=settings.url_settings.register_url) as client:
        yield client
