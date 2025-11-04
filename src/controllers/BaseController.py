from helpers.config import Settings,get_settings
from fastapi import APIRouter, FastAPI, Depends, UploadFile
import os
import random
import string
class BaseController:
    def __init__(self, app_settings: Settings = Depends(get_settings)):
        self.app_settings = app_settings
        self.dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.dir, "assets/files")

    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))