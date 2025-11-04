from fastapi import APIRouter, FastAPI, Depends, UploadFile
from controllers import DataController
from helpers.config import Settings, get_settings
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile, 
                      app_settings: Settings = Depends(get_settings)):
    #validate file properties
    is_valid, message = DataController(app_settings).validate_file(file)
    if not is_valid:
        return {"error": message}
    return {"message": message}