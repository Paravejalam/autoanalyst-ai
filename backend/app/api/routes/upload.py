from fastapi import APIRouter, UploadFile, File
from app.services.file_service import save_upload_file
from app.schemas.response import StandardResponse, UploadResponseData
from app.core.logger import logger

router = APIRouter()

@router.post("/upload", response_model=StandardResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a data file (CSV or Excel) and returns a unique file ID.
    """
    logger.info(f"Upload request received for file: {file.filename}")
    file_id, file_name, _ = save_upload_file(file)
    
    return StandardResponse(
        status="success",
        data=UploadResponseData(
            file_id=file_id,
            filename=file_name
        )
    )
