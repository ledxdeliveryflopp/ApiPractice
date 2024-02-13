from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, password: str):
    """Проверка пароля"""
    return pwd_context.verify(plain_password, password)
