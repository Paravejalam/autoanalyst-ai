import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException
from app.core.logger import logger

# Build absolute path to backend/uploads
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def save_upload_file(upload_file: UploadFile) -> tuple[str, str, str]:
    if upload_file.size is not None:
        if upload_file.size == 0:
            logger.error(f"Empty file uploaded: {upload_file.filename}")
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")
        if upload_file.size > MAX_FILE_SIZE:
            logger.error(f"File size exceeds limit: {upload_file.size} bytes")
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 5MB.")
    _, ext = os.path.splitext(upload_file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        logger.error(f"Invalid file extension: {ext}")
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV and Excel files are allowed.")
    
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        logger.info(f"File saved successfully: {file_path}")
        return file_id, file_name, file_path
    except Exception as e:
        logger.error(f"Error saving file {upload_file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to save file.")

def get_file_path(file_id: str) -> str:
    for file in os.listdir(UPLOAD_FOLDER):
        if file.startswith(file_id):
            return os.path.join(UPLOAD_FOLDER, file)
    logger.error(f"File not found: {file_id}")
    raise HTTPException(status_code=404, detail="File not found")
