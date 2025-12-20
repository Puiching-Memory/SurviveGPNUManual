"""
Storage 配置模块

提供现代、可扩展的存储目录结构定义和管理。

目录结构：
storage/
├── data/              # 数据文件（持久化存储）
│   ├── documents/     # 文档内容
│   ├── assets/        # 资源文件
│   │   ├── shared/    # 共享资源
│   │   └── {doc_id}/  # 文档专属资源
│   ├── attachments/   # 附件
│   └── uploads/       # 用户上传文件
├── cache/             # 缓存文件（可清理）
│   └── thumbnails/    # 缩略图缓存
└── temp/              # 临时文件（定期清理）
"""

import os
from pathlib import Path
from typing import Optional
from functools import lru_cache

# Base directory setup
def _get_storage_root() -> Path:
    """Get storage root directory."""
    # Calculate relative to this file location
    config_dir = Path(__file__).parent
    backend_dir = config_dir.parent
    return backend_dir.parent / "storage"

# Get storage root
_STORAGE_ROOT = _get_storage_root()

# Data directories (persistent storage)
DATA_DIR = _STORAGE_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
ASSETS_DIR = DATA_DIR / "assets"
ATTACHMENTS_DIR = DATA_DIR / "attachments"
UPLOADS_DIR = DATA_DIR / "uploads"

# Cache directories (can be cleared)
CACHE_DIR = _STORAGE_ROOT / "cache"
THUMBNAILS_DIR = CACHE_DIR / "thumbnails"

# Temporary directories (should be cleaned periodically)
TEMP_DIR = _STORAGE_ROOT / "temp"

# Maximum upload size (100MB)
MAX_UPLOAD_SIZE = 100 * 1024 * 1024


def ensure_storage_directories() -> None:
    """
    确保所有存储目录存在
    
    在应用启动时调用，创建必要的目录结构。
    """
    directories = [
        # Data directories
        DOCUMENTS_DIR,
        ASSETS_DIR,
        ASSETS_DIR / "shared",
        ATTACHMENTS_DIR,
        UPLOADS_DIR,
        # Cache directories
        CACHE_DIR,
        THUMBNAILS_DIR,
        # Temporary directories
        TEMP_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_asset_dir(doc_id: Optional[str] = None) -> Path:
    """
    获取资源文件目录
    
    Args:
        doc_id: 文档ID，如果提供则返回文档专属目录，否则返回共享目录
        
    Returns:
        资源文件目录路径
    """
    if doc_id:
        return ASSETS_DIR / str(doc_id)
    return ASSETS_DIR / "shared"


def get_cache_path(relative_path: str) -> Path:
    """
    获取缓存文件路径
    
    Args:
        relative_path: 相对于缓存目录的相对路径
        
    Returns:
        缓存文件完整路径
    """
    return CACHE_DIR / relative_path


def get_temp_path(filename: Optional[str] = None) -> Path:
    """
    获取临时文件路径
    
    Args:
        filename: 文件名，如果提供则返回完整路径，否则只返回临时目录
        
    Returns:
        临时文件路径
    """
    if filename:
        return TEMP_DIR / filename
    return TEMP_DIR


def clear_temp_files() -> int:
    """
    清理临时文件
    
    Returns:
        删除的文件数量
    """
    count = 0
    if TEMP_DIR.exists():
        for file in TEMP_DIR.iterdir():
            if file.is_file():
                try:
                    file.unlink()
                    count += 1
                except Exception:
                    pass
    return count


# Storage root
STORAGE_ROOT = _STORAGE_ROOT

