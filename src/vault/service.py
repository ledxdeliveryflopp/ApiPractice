import hvac
from src.settings.settings import Settings

settings = Settings()

client = hvac.Client(
    url=settings.vault_url,
    token=settings.vault_token,
)


async def create_secret(email: str, password: str):
    """Сохранение секрета в vault"""
    new_secret = client.secrets.kv.v2.create_or_update_secret(
        mount_point=settings.vault_mount,
        path=f'{email}-secret-password',
        secret=dict(password=f"{password}"),
    )
    return new_secret


async def read_secret(email: str):
    """Чтение секрета из vault"""
    secret_by_vault = client.secrets.kv.read_secret_version(mount_point=settings.vault_mount,
                                                            path=f'{email}-secret-password')
    secret = secret_by_vault["data"]["data"]["password"]
    return secret
