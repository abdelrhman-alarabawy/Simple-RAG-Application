import re, os
from .BaseController import BaseController
from .ProjectController import ProjectController
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

    def generate_unique_filepath(self, orig_file_name: str, project_id: str):

            random_key = self.generate_random_string()
            project_path = ProjectController().get_project_path(project_id=project_id)

            cleaned_file_name = self.get_clean_file_name(
                orig_file_name=orig_file_name
            )

            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

            while os.path.exists(new_file_path):
                random_key = self.generate_random_string()
                new_file_path = os.path.join(
                    project_path,
                    random_key + "_" + cleaned_file_name
                )

            return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, orig_file_name: str):

            # remove any special characters, except underscore and .
            cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

            # replace spaces with underscore
            cleaned_file_name = cleaned_file_name.replace(" ", "_")

            return cleaned_file_name