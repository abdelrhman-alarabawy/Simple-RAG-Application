from fastapi import APIRouter, FastAPI
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome():
    app_name, app_version = os.getenv("APP_NAME"), os.getenv("APP_VERSION")
    return {
        "message": f"Welcome to the {app_name} API (v{app_version})!"
    }
