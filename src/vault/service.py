from dataclasses import dataclass
import hvac
import hvac.exceptions
from src.settings.exceptions import VaultInvalidPath, VaultInvalidSealed
from src.settings.settings import settings


@dataclass
class VaultService:
    client = hvac.Client(
        url=settings.vault_settings.vault_url,
        token=settings.vault_settings.vault_token_app,
    )

    async def create_secret(self, user_id: int, password: str):
        """Сохранение секрета в vault"""
        try:
            new_secret = self.client.secrets.kv.v2.create_or_update_secret(
                mount_point=settings.vault_settings.vault_mount,
                path=f'{user_id}-secret-password',
                secret=dict(password=f"{password}"),
            )
            return new_secret
        except hvac.exceptions.VaultDown:
            raise VaultInvalidSealed

    async def read_secret(self, user_id: int):
        """Чтение секрета из vault"""
        try:
            secret_by_vault = self.client.secrets.kv.read_secret_version(
                mount_point=settings.vault_settings.vault_mount, path=f'{user_id}-secret-password')
            secret = secret_by_vault["data"]["data"]["password"]
            return secret
        except hvac.exceptions.InvalidPath:
            raise VaultInvalidPath
