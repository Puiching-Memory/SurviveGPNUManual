from fastapi import APIRouter
from app.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


@router.get("/health", tags=["Health"])
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}
