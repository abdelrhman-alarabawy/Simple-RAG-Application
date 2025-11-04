import os
import aiofiles
from fastapi import APIRouter, FastAPI, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from models import ResponseStatus
import logging

logger = logging.getLogger('uvicorn.error')

from controllers import DataController, ProjectController
from helpers.config import Settings, get_settings
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile, 
                      app_settings: Settings = Depends(get_settings)):
    #validate file properties
    data_controller = DataController(app_settings)
    is_valid, message = data_controller.validate_file(file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={
                "error": message
            }
        )
    
    project_dir_path = ProjectController().get_project_path(project_id)


    # file_path = os.path.join(project_dir_path, file.filename)
    file_path = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    try:
        async with aiofiles.open(file_path, "wb") as f:
                    while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                        await f.write(chunk)

    except Exception as e:

        logger.error(f"File upload failed: {e}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message":ResponseStatus.FILE_UPLOAD_FAILURE
            }
        )

    return JSONResponse(
        content={
            "message": ResponseStatus.FILE_UPLOAD_SUCCESS,
        }
    )

   