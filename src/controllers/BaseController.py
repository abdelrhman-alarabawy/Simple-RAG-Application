from helpers.config import Settings,get_settings
from fastapi import APIRouter, FastAPI, Depends, UploadFile

class BaseController:
    def __init__(self, app_settings: Settings = Depends(get_settings)):
        self.app_settings = app_settings