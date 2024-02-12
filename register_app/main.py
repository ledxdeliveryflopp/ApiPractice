from fastapi import FastAPI
from src.router import router

register = FastAPI()

register.include_router(router)
