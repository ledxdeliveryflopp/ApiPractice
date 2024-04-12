import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware
from src.authorization.router import authorization_router
from src.password.router import password_router
from src.registration.models import UserModel, Role
from src.registration.router import register_router
from src.registration.utils import hash_password
from src.settings.db import engine, Base
from src.vault.service import VaultService

authorization = FastAPI()


origins: list[str] = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:7000",
    "http://localhost:6000",
    "http://localhost:5000",
]

authorization.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


authorization.include_router(authorization_router)
authorization.include_router(register_router)
authorization.include_router(password_router)


async def init_tables():
    """Создание таблиц"""
    async with engine.begin() as conn:
        user_table = await conn.run_sync(lambda sync_conn: inspect(sync_conn).has_table("user"))
        token_table = await conn.run_sync(lambda sync_conn: inspect(sync_conn).has_table("token"))
        code_table = await conn.run_sync(lambda sync_conn: inspect(sync_conn).has_table("code"))
        if not user_table or not token_table or not code_table:
            await conn.run_sync(Base.metadata.create_all)


async def init_admin_and_manager():
    """Создание администратора и менеджера"""
    async with AsyncSession(engine) as session:
        try:
            admin_user = UserModel(id=1, username="admin", email="admin@admin.ru",
                                   role=Role.admin)
            manager_user = UserModel(id=2, username="manager", email="manager@manager.ru",
                                     role=Role.manager)
            session.add(admin_user)
            session.add(manager_user)
            await session.commit()
        except sqlalchemy.exc.IntegrityError:
            await session.rollback()

@authorization.on_event("startup")
async def init():
    await init_tables()
    await init_admin_and_manager()
    vault = VaultService()
    await vault.create_secret(user_id=1, password=hash_password(password="admin"))
    await vault.create_secret(user_id=2, password=hash_password(password="manager"))
