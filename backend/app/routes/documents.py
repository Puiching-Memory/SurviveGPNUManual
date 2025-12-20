from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID
from pathlib import Path
import tempfile

from app.db.database import get_db
from app.db.models import User
from app.routes.auth import get_current_user, require_admin
from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    ImportOptions,
    ImportResult
)
from app.services.document_service import DocumentService
from app.services.package_service import PackageService
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


@router.post("/import-package", response_model=ImportResult)
async def import_package(
    file: UploadFile = File(...),
    conflict_strategy: str = Query("skip", regex="^(skip|overwrite|rename)$"),
    import_assets: bool = Query(True),
    import_attachments: bool = Query(True),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Import documents from .gpnu package (admin only)."""
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gpnu") as temp_file:
        temp_path = Path(temp_file.name)
        try:
            # Write uploaded file
            content = await file.read()
            temp_path.write_bytes(content)
            
            # Import package
            package_service = PackageService(db)
            options = ImportOptions(
                conflict_strategy=conflict_strategy,
                import_assets=import_assets,
                import_attachments=import_attachments
            )
            result = await package_service.import_package(temp_path, current_user, options)
            return result
        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()


@router.get("/export-package")
async def export_package(
    category: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    published: Optional[bool] = Query(None),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Export documents to .gpnu package (admin only)."""
    tag_list = [t.strip() for t in tags.split(",")] if tags else None
    
    package_service = PackageService(db)
    package_path = await package_service.export_package(
        current_user,
        category=category,
        tags=tag_list,
        published=published
    )
    
    return FileResponse(
        package_path,
        media_type="application/zip",
        filename="documents.gpnu",
        background=None
    )


@router.post("/validate-package")
async def validate_package(
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin)
):
    """Validate .gpnu package format (admin only)."""
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.db.database import AsyncSessionLocal
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gpnu") as temp_file:
        temp_path = Path(temp_file.name)
        try:
            content = await file.read()
            temp_path.write_bytes(content)
            
            # Validate
            async with AsyncSessionLocal() as db:
                package_service = PackageService(db)
                is_valid, error_msg = await package_service.validate_package(temp_path)
                
                return {
                    "valid": is_valid,
                    "error": error_msg
                }
        finally:
            if temp_path.exists():
                temp_path.unlink()


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
    asset_path = AssetService.get_shared_asset_dir() / filename
    if not asset_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return FileResponse(asset_path)

