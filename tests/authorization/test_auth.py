import pytest
from httpx import AsyncClient
from src.settings.settings import Settings

settings = Settings()


@pytest.mark.asyncio
async def test_success_authorization():
    """Тест удачной авторизации"""
    async with AsyncClient() as client:
        response = await client.post(url=f'{settings.auth_url}/login/',
                                     json={"email": "korstim18@gmail.com", "password": "stringst"})
        assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_failed_authorization():
    """Тест регистрации при не верных данных"""
    async with AsyncClient() as client:
        response = await client.post(url=f'{settings.auth_url}/login/',
                                     json={"email": "bruh@mail.com", "password": "3412412"})
        assert response.status_code == 403
        assert response.json() == {"detail": "Incorrect email or password."}
