from fastapi import APIRouter, FastAPI
import os
from helpers.config import Settings
base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome():
    settings = Settings()
    return {
        "message": f"Welcome to the {settings.APP_NAME} API (v{settings.APP_VERSION})!"
    }
