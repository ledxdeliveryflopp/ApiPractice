import json

import pytest
from httpx import AsyncClient
from src.settings.settings import Settings

settings = Settings()


@pytest.mark.asyncio
async def test_success_authorization():
    """Тест удачной авторизации"""
    async with AsyncClient() as client:
        response = await client.post(url=f'{settings.auth_url}/login/',
                                     json={"email": "test@test.ru", "password": "DSTAWAR$WA@5#a2"})
        assert response.status_code == 200
        assert response.json() == response.json()


@pytest.mark.asyncio
async def test_failed_authorization_bad_email_format():
    """Тест неудачной авторизации, не верный формат почты"""
    async with AsyncClient() as client:
        response = await client.post(url=f'{settings.auth_url}/login/',
                                     json={"email": "admintsemil.com", "password": "3412412"})
        assert response.status_code == 422
        assert response.json() == response.json()


@pytest.mark.asyncio
async def test_failed_authorization_bad_password():
    """Тест неудачной авторизации, не верный пароль"""
    async with AsyncClient() as client:
        response = await client.post(url=f'{settings.auth_url}/login/',
                                     json={"email": "test@test.ru", "password": "3412412"})
        assert response.status_code == 403
        assert response.json() == {"detail": "Incorrect email or password."}
