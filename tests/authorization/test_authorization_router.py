from starlette import status


class TestAuthorization:
    url: str = "/login/"
    json_success: dict = {"email": "test@test.ru", "password": "testprofilepassword"}
    json_failed: dict = {"email": "test@test.ru", "password": ""}

    async def test_success_login(self, AuthClient):
        """Тест успешной авторизации"""
        response = await AuthClient.post(url=self.url, json=self.json_success)
        assert response.status_code == status.HTTP_200_OK

    async def test_bad_credentials_login(self, AuthClient):
        """Тест валидации авторизации"""
        response = await AuthClient.post(url=self.url, json=self.json_failed)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Incorrect email or password."}
