import pytest
from httpx import AsyncClient
from src.settings.settings import Settings

settings = Settings()


@pytest.mark.asyncio
async def test_success_register():
    """Тест удачной регистрации"""
    async with AsyncClient() as client:
        response = await client.post(url=f'{settings.register_url}/register/',
                                     json={"username": "test", "email": "test@test.ru",
                                           "password": "DSTAWAR$WA@5#a2"})
        assert response.status_code == 200
        assert response.json() == {"username": "test", "email": "test@test.ru"}


@pytest.mark.asyncio
async def test_failed_register():
    """Тест регистрации при не верных форматах полей"""
    async with AsyncClient() as client:
        response = await client.post(url=f'{settings.register_url}/register/',
                                     json={"username": "test", "email": "test.ru",
                                           "password": "DSTA"})
        assert response.status_code == 422


@pytest.mark.asyncio
async def duplicate_register(t):
    """Тест регистрации существующего пользователя"""
    async with AsyncClient() as client:
        response = await client.post(url=f'{settings.register_url}/register/',
                                     json={"username": "test", "email": "test@test.ru",
                                           "password": "DSTAWAR$WA@5#a2"})
        assert response.status_code == 400
        assert response.json() == {"detail": "User already exist."}
