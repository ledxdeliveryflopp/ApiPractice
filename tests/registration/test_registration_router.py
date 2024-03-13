from starlette import status


class TestRegistration:
    url: str = "/register/"
    json_success: dict = {"username": "TestRegister", "email": "testregister@test.ru", "password":
                          "testprofilepassword"}
    json_duplicate: dict = {"username": "test", "email": "test@test.ru", "password": "testesat"}
    json_failed_email: dict = {"email": "testtest", "password": "rewq34242434"}
    json_failed_password: dict = {"email": "test2@test.ru", "password": "tst"}

    async def test_success_registration(self, RegisterClient):
        """Тест успешной регистрации"""
        response = await RegisterClient.post(url=self.url, json=self.json_success)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"username": "TestRegister", "email": "testregister@test.ru"}

    async def test_validation_duplicate_failed_registration(self, RegisterClient):
        """Тест неудачной валидации из-за дубликата при регистрации"""
        response = await RegisterClient.post(url=self.url, json=self.json_duplicate)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "User already exist."}

    async def test_validation_bad_email_failed_registration(self, RegisterClient):
        """Тест неудачной валидации из-за не правильной почты при регистрации"""
        response = await RegisterClient.post(url=self.url, json=self.json_failed_email)
        print("test3", response.json())

    async def test_validation_bad_password_failed_registration(self, RegisterClient):
        """Тест неудачной валидации из-за не правильной длины пароля при регистрации"""
        response = await RegisterClient.post(url=self.url, json=self.json_failed_password)
        print("test4", response.json())
