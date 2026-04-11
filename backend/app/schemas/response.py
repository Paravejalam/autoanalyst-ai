from pydantic import BaseModel
from typing import Any, Dict, List

class StandardResponse(BaseModel):
    status: str
    data: Any

class UploadResponseData(BaseModel):
    file_id: str
    filename: str

class AnalysisResponseData(BaseModel):
    summary: str
    insights: List[str]
    statistics: Dict[str, Any]
