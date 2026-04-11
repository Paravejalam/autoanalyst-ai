import pandas as pd
from openai import AsyncOpenAI
import json
from typing import Tuple, List, Dict, Any
from app.core.config import settings
from app.core.logger import logger

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_insights(df: pd.DataFrame, summary_stats: Dict[str, Any]) -> Tuple[str, List[str]]:
    """
    Leverages OpenAI to analyze the extracted summary statistics from the dataset.
    """
    # Guard clause if no API key is present or it's clearly a placeholder
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
        logger.warning("No valid OPENAI_API_KEY provided. Returning mock insights.")
        return "No API key config found.", ["Mock Insight 1: Please set a valid OPENAI_API_KEY in .env"]

    try:
        prompt = f"""
        Analyze the following dataset summary and provide a brief overall summary and key insights.
        
        Dataset Statistics:
        Columns: {summary_stats.get('columns_count')}
        Rows: {summary_stats.get('rows')}
        Columns list: {', '.join(summary_stats.get('columns', []))}
        
        Return the result EXACTLY as a JSON object with this schema:
        {{
            "summary": "a short paragraph describing the dataset",
            "insights": ["insight 1", "insight 2", "insight 3"]
        }}
        """
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert data analyst AI."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result_content = response.choices[0].message.content
        if result_content:
            data = json.loads(result_content)
            return data.get("summary", "Analysis complete."), data.get("insights", [])
        return "Empty response from AI.", []
        
    except Exception as e:
        logger.error(f"Error in AI service: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=502, detail=f"AI service integration failed: {str(e)}")