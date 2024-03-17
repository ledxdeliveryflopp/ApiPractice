from dataclasses import dataclass
from typing import Any
from src.settings.repository import SessionRepository


@dataclass
class SessionService:
    session_repository: SessionRepository

    async def get_object_by_parameter(self, model: Any, email: str):
        data = await self.session_repository.session_find_by_parameter(model=model,
                                                                       email=email)
        return data

    async def get_token(self, model: Any, token: str):
        data = await self.session_repository.session_find_token(model=model, token=token)
        return data

    async def create_object(self, save_object: dict):
        data = await self.session_repository.session_add(save_object=save_object)
        return data

    async def delete_object(self, delete_object: dict):
        data = await self.session_repository.session_delete(delete_object=delete_object)
        return data

