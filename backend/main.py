from fastapi import FastAPI, UploadFile, File
import shutil
import os

from ml.data_processing import process_data

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AutoAnalyst AI Running 🚀"}


@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = process_data(file_path)

    return {
        "status": "success",
        "analysis": result
    }