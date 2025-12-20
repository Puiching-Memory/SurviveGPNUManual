from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.utils.logger import setup_logger
from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.documents import router as documents_router
from app.routes.filesystem_documents import router as filesystem_documents_router
from app.db.database import init_db, engine
from app.db.models import User, Document  # Import models to ensure they are registered
from app.config import get_settings, ASSETS_DIR, DOCUMENTS_DIR, UPLOADS_DIR, ATTACHMENTS_DIR

settings = get_settings()
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting application")
    try:
        await init_db()
        logger.info("Application started successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        # Cleanup
        logger.info("Shutting down application")
        await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(filesystem_documents_router, prefix="/api")

# Ensure storage directories exist (new modern structure)
ensure_storage_directories()

# Mount static files for assets
shared_assets_dir = ASSETS_DIR / "shared"
app.mount("/api/documents/assets/shared", StaticFiles(directory=str(shared_assets_dir)), name="shared-assets")
app.mount("/api/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

logger.info("Application routes configured")
