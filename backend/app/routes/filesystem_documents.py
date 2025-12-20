"""
文件系统文档路由

直接从文件系统读取和提供文档内容，不依赖数据库。
"""

from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import Response
from typing import Optional, List
from pathlib import Path

from app.services.filesystem_document_service import FilesystemDocumentService
from app.config import DOCUMENTS_DIR, ASSETS_DIR
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/filesystem-documents", tags=["filesystem-documents"])


@router.get("")
async def list_documents(
    category: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),  # 逗号分隔的标签
    published: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    列出所有文档
    
    直接从文件系统读取，不依赖数据库。
    """
    tag_list = [t.strip() for t in tags.split(",")] if tags else None
    
    service = FilesystemDocumentService()
    try:
        documents = await service.list_documents(
            category=category,
            tags=tag_list,
            published=published,
            skip=skip,
            limit=limit
        )
        # 注意：total 是当前返回的文档数量，不是总数
        # 如果需要准确的总数，需要额外查询（但会影响性能）
        return {"documents": documents, "total": len(documents)}
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing documents: {str(e)}"
        )


@router.get("/{slug}")
async def get_document(slug: str):
    """
    根据 slug 获取文档
    
    返回完整的文档信息，包括内容。
    """
    service = FilesystemDocumentService()
    try:
        document = await service.get_by_slug(slug)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with slug '{slug}' not found"
            )
        return document
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document {slug}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document: {str(e)}"
        )


@router.get("/{slug}/content")
async def get_document_content(slug: str):
    """
    获取文档内容（仅 markdown 文本）
    """
    service = FilesystemDocumentService()
    try:
        content = await service.read_content(slug)
        if content is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with slug '{slug}' not found"
            )
        return Response(content=content, media_type="text/markdown; charset=utf-8")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document content {slug}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document content: {str(e)}"
        )


@router.get("/by-path/{path:path}")
async def get_document_by_path(path: str):
    """
    根据路径获取文档
    
    路径相对于 storage/data/documents 目录（支持主题分类子目录）。
    """
    service = FilesystemDocumentService()
    try:
        document = await service.get_by_path(path)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document at path '{path}' not found"
            )
        return document
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document at path {path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document: {str(e)}"
        )

