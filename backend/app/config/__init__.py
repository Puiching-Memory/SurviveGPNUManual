"""Configuration Module"""

from .config import (
    Settings,
    get_settings,
    CURRENT_LOGGING_CONFIG,
    ensure_storage_directories,
)
from .storage import (
    STORAGE_ROOT,
    DOCUMENTS_DIR,
    ASSETS_DIR,
    ATTACHMENTS_DIR,
    UPLOADS_DIR,
    MAX_UPLOAD_SIZE,
    get_asset_dir,
    get_cache_path,
    get_temp_path,
)

__all__ = [
    "Settings",
    "get_settings",
    "CURRENT_LOGGING_CONFIG",
    "ensure_storage_directories",
    "STORAGE_ROOT",
    "DOCUMENTS_DIR",
    "ASSETS_DIR",
    "ATTACHMENTS_DIR",
    "UPLOADS_DIR",
    "MAX_UPLOAD_SIZE",
    "get_asset_dir",
    "get_cache_path",
    "get_temp_path",
]
