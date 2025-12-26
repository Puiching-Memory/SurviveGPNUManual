from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID
from pathlib import Path

from app.db.database import get_db
from app.db.models import User
from app.routes.auth import get_current_user, require_admin
from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse
)
from app.services.document_service import DocumentService
from app.services.asset_service import AssetService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    category: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),  # Comma-separated
    published: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """List documents with optional filters."""
    tag_list = [t.strip() for t in tags.split(",")] if tags else None
    
    doc_service = DocumentService(db)
    documents = await doc_service.list_documents(
        category=category,
        tags=tag_list,
        published=published,
        skip=skip,
        limit=limit
    )
    return documents


@router.get("/{slug}", response_model=DocumentResponse)
async def get_document(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a document by slug."""
    doc_service = DocumentService(db)
    document = await doc_service.get_by_slug(slug)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with slug '{slug}' not found"
        )
    return document


@router.get("/{slug}/content")
async def get_document_content(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get document content."""
    doc_service = DocumentService(db)
    document = await doc_service.get_by_slug(slug)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with slug '{slug}' not found"
        )
    
    try:
        content = await doc_service.read_content(document)
        return {"content": content}
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document content file not found"
        )


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    doc_data: DocumentCreate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Create a new document (admin only)."""
    doc_service = DocumentService(db)
    try:
        document = await doc_service.create_document(doc_data, author_id=current_user.id)
        return document
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{doc_id}", response_model=DocumentResponse)
async def update_document(
    doc_id: UUID,
    doc_data: DocumentUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Update a document (admin only)."""
    doc_service = DocumentService(db)
    try:
        document = await doc_service.update_document(doc_id, doc_data)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with id '{doc_id}' not found"
            )
        return document
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    doc_id: UUID,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Delete a document (admin only)."""
    doc_service = DocumentService(db)
    success = await doc_service.delete_document(doc_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id '{doc_id}' not found"
        )
# Asset routes
@router.get("/assets/{doc_id}/{filename:path}")
async def get_asset(
    doc_id: UUID,
    filename: str
):
    """Get an asset file."""
    asset_path = AssetService.get_asset_dir(doc_id) / filename
    if not asset_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return FileResponse(asset_path)


@router.get("/assets/shared/{filename:path}")
async def get_shared_asset(filename: str):
    """Get a shared asset file."""
    # URL decode the filename to handle Chinese characters
    import urllib.parse
    decoded_filename = urllib.parse.unquote(filename)
    
    asset_dir = AssetService.get_shared_asset_dir()
    asset_path = asset_dir / decoded_filename
    
    if not asset_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return FileResponse(asset_path)

