from fastapi import APIRouter
from app.schemas.request import AnalyzeRequest
from app.schemas.response import StandardResponse, AnalysisResponseData
from app.services.analysis_service import analyze_file
from app.core.logger import logger

router = APIRouter()

@router.post("/analyze", response_model=StandardResponse)
async def analyze_data(request: AnalyzeRequest):
    """
    Analyzes an uploaded file by its file ID, returning data summaries and AI insights.
    """
    logger.info(f"Analyze request received for file_id: {request.file_id}")
    result = await analyze_file(request.file_id)
    
    return StandardResponse(
        status="success",
        data=AnalysisResponseData(
            summary=result["summary"],
            insights=result["insights"],
            statistics=result["statistics"]
        )
    )
