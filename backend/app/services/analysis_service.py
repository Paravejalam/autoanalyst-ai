from typing import Dict, Any
from app.services.file_service import get_file_path
from app.services.ai_service import generate_insights
from ml.pipelines.pipeline import process_file_data
from app.core.logger import logger

async def analyze_file(file_id: str) -> Dict[str, Any]:
    """
    Orchestrates the data pipeline and AI insights generation for a given file ID.
    """
    logger.info(f"Starting analysis for file_id: {file_id}")
    file_path = get_file_path(file_id)
    
    from fastapi import HTTPException
    
    logger.info("Processing data pipeline...")
    try:
        df_cleaned, summary = process_file_data(file_path)
    except ValueError as e:
        logger.error(f"Data processing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in data processing: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during data processing.")
    
    logger.info("Generating AI insights...")
    ai_summary, insights = await generate_insights(df_cleaned, summary)
    
    logger.info("Analysis completed successfully.")
    return {
        "summary": ai_summary,
        "insights": insights,
        "statistics": summary
    }
