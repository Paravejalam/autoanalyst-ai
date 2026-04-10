from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import upload, analysis
from app.core.config import settings
from app.core.logger import logger
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for AutoAnalyst AI platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(upload.router, tags=["Upload"])
app.include_router(analysis.router, tags=["Analysis"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting AutoAnalyst AI Backend...")

@app.get("/", tags=["Health"])
def home():
    return {"message": f"{settings.PROJECT_NAME} API Running"}
