from .BaseController import BaseController
from fastapi import APIRouter, FastAPI, Depends, UploadFile
from models import ResponseStatus

class DataController(BaseController):
    def __init__(self, app_settings = ...):
        super().__init__(app_settings)

    def validate_file(self, file: UploadFile) -> bool:
        # Check file extension
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseStatus.FILE_TYPE_NOT_SUPPORTED

        # Check file size
        file.file.seek(0, 2)  # Move to end of file
        file_size = file.file.tell()  # Get current position (size)
        file.file.seek(0)  # Reset to start of file

        max_size_bytes = self.app_settings.FILE_MAX_SIZE_MB * 1024 * 1024
        if file_size > max_size_bytes:
            return False, ResponseStatus.FILE_SIZE_EXCEEDED

        return True, ResponseStatus.FILE_VALIDATION_SUCCESS