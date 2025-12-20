import zipfile
import json
import tempfile
from pathlib import Path
from typing import Optional, Dict, List
from uuid import UUID, uuid4
from datetime import datetime
import aiofiles
import shutil

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Document, User
from app.schemas.document import (
    DocumentPackageManifest,
    DocumentInManifest,
    ImportOptions,
    ImportResult,
    DocumentCreate,
    DocumentAuthor
)
from app.services.document_service import DocumentService
from app.services.asset_service import AssetService
from app.config import get_settings
from app.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)


class PackageService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.doc_service = DocumentService(db)

    async def validate_package(self, zip_path: Path) -> tuple:
        """Validate .gpnu package format."""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Check for manifest.json
                if 'manifest.json' not in zip_file.namelist():
                    return False, "manifest.json not found in package"
                
                # Try to parse manifest.json
                manifest_data = json.loads(zip_file.read('manifest.json').decode('utf-8'))
                
                # Validate required fields
                required_fields = ['format_version', 'exported_at', 'exported_by', 'documents']
                for field in required_fields:
                    if field not in manifest_data:
                        return False, f"Missing required field: {field}"
                
                # Validate documents
                doc_slugs = set()
                doc_ids = set()
                for doc in manifest_data.get('documents', []):
                    if 'id' not in doc or 'slug' not in doc or 'file_path' not in doc:
                        return False, "Invalid document entry in manifest"
                    
                    # Check for duplicate slugs
                    if doc['slug'] in doc_slugs:
                        return False, f"Duplicate slug: {doc['slug']}"
                    doc_slugs.add(doc['slug'])
                    
                    # Check for duplicate IDs
                    doc_id = doc['id']
                    if doc_id in doc_ids:
                        return False, f"Duplicate document ID: {doc_id}"
                    doc_ids.add(doc_id)
                    
                    # Check if file exists
                    if doc['file_path'] not in zip_file.namelist():
                        return False, f"Document file not found: {doc['file_path']}"
                
                return True, None
        except zipfile.BadZipFile:
            return False, "Invalid ZIP file"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON in manifest.json: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    async def parse_manifest(self, zip_path: Path) -> DocumentPackageManifest:
        """Parse manifest.json from package."""
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            manifest_data = json.loads(zip_file.read('manifest.json').decode('utf-8'))
            return DocumentPackageManifest(**manifest_data)

    async def import_package(
        self,
        zip_path: Path,
        user: User,
        options: ImportOptions
    ) -> ImportResult:
        """Import documents from .gpnu package."""
        result = ImportResult(
            success=False,
            total=0,
            imported=0,
            skipped=0,
            failed=0,
            errors=[]
        )
        
        try:
            # Validate package
            is_valid, error_msg = await self.validate_package(zip_path)
            if not is_valid:
                result.errors.append(f"Package validation failed: {error_msg}")
                return result
            
            # Parse manifest
            manifest = await self.parse_manifest(zip_path)
            result.total = len(manifest.documents)
            
            # Extract to temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                with zipfile.ZipFile(zip_path, 'r') as zip_file:
                    zip_file.extractall(temp_path)
                
                # Import each document
                for doc_manifest in manifest.documents:
                    try:
                        # Check if document exists
                        existing = await self.doc_service.get_by_slug(doc_manifest.slug)
                        
                        if existing:
                            if options.conflict_strategy == "skip":
                                result.skipped += 1
                                continue
                            elif options.conflict_strategy == "overwrite":
                                # Delete existing document
                                await self.doc_service.delete_document(existing.id)
                            elif options.conflict_strategy == "rename":
                                # Generate new slug
                                doc_manifest.slug = f"{doc_manifest.slug}-{uuid4().hex[:8]}"
                        
                        # Read document content
                        doc_file_path = temp_path / doc_manifest.file_path
                        if not doc_file_path.exists():
                            result.failed += 1
                            result.errors.append(f"Document file not found: {doc_manifest.file_path}")
                            continue
                        
                        async with aiofiles.open(doc_file_path, 'r', encoding='utf-8') as f:
                            content = await f.read()
                        
                        # Create document
                        doc_create = DocumentCreate(
                            slug=doc_manifest.slug,
                            title=doc_manifest.title,
                            file_path=f"content/{doc_manifest.id}.md",
                            category=doc_manifest.category,
                            published=doc_manifest.published,
                            tags=doc_manifest.tags or [],
                            relations=doc_manifest.relations or [],
                            extra_metadata=doc_manifest.frontmatter or {}
                        )
                        
                        document = await self.doc_service.create_document(
                            doc_create,
                            author_id=user.id
                        )
                        
                        # Write content
                        await self.doc_service.write_content(document, content)
                        
                        # Import assets
                        if options.import_assets:
                            for asset_path in doc_manifest.assets:
                                asset_source = temp_path / asset_path
                                if asset_source.exists():
                                    is_shared = "shared" in asset_path
                                    await AssetService.copy_asset(
                                        asset_source,
                                        document.id,
                                        asset_source.name,
                                        is_shared=is_shared
                                    )
                        
                        result.imported += 1
                        
                    except Exception as e:
                        result.failed += 1
                        result.errors.append(f"Failed to import {doc_manifest.slug}: {str(e)}")
                        logger.error(f"Error importing document {doc_manifest.slug}: {e}")
                
                result.success = result.failed == 0
                
        except Exception as e:
            result.errors.append(f"Import failed: {str(e)}")
            logger.error(f"Package import error: {e}")
        
        return result

    async def export_package(
        self,
        user: User,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        published: Optional[bool] = None
    ) -> Path:
        """Export documents to .gpnu package."""
        # Get documents
        documents = await self.doc_service.list_documents(
            category=category,
            tags=tags,
            published=published,
            limit=10000  # Large limit for export
        )
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)
        
        try:
            # Create directory structure
            content_dir = temp_path / "content"
            assets_dir = temp_path / "assets"
            content_dir.mkdir()
            assets_dir.mkdir()
            
            # Build manifest
            doc_manifests = []
            total_assets = 0
            
            for doc in documents:
                # Read content
                try:
                    content = await self.doc_service.read_content(doc)
                except Exception as e:
                    logger.warning(f"Failed to read content for {doc.slug}: {e}")
                    continue
                
                # Write content file
                content_file = content_dir / f"{doc.id}.md"
                async with aiofiles.open(content_file, 'w', encoding='utf-8') as f:
                    await f.write(content)
                
                # Collect assets
                doc_assets = []
                asset_list = await AssetService.list_assets(doc.id)
                for asset_path in asset_list:
                    asset_rel_path = f"assets/{doc.id}/{asset_path.name}"
                    doc_assets.append(asset_rel_path)
                    
                    # Copy asset to package
                    package_asset_dir = assets_dir / str(doc.id)
                    package_asset_dir.mkdir(exist_ok=True)
                    shutil.copy2(asset_path, package_asset_dir / asset_path.name)
                    total_assets += 1
                
                # Build document manifest entry
                doc_author = DocumentAuthor(
                    user_id=doc.author_id,
                    username=user.username if doc.author_id == user.id else None,
                    email=user.email if doc.author_id == user.id else None
                )
                
                doc_manifest = DocumentInManifest(
                    id=doc.id,
                    file_path=f"content/{doc.id}.md",
                    slug=doc.slug,
                    title=doc.title,
                    category=doc.category,
                    tags=doc.tags or [],
                    authors=[doc_author] if doc.author_id else [],
                    created_at=doc.created_at,
                    updated_at=doc.updated_at,
                    published=doc.published,
                    frontmatter=doc.extra_metadata or {},
                    relations=doc.relations or [],
                    assets=doc_assets,
                    attachments=[]
                )
                doc_manifests.append(doc_manifest)
            
            # Create manifest.json
            from app.schemas.document import PackageExportedBy, PackageStatistics
            
            manifest = DocumentPackageManifest(
                format_version="1.0",
                format_spec="https://github.com/your-org/gpnu-format-spec",
                exported_at=datetime.utcnow(),
                exported_by=PackageExportedBy(
                    user_id=user.id,
                    email=user.email,
                    username=user.username
                ),
                package_info=None,
                statistics=PackageStatistics(
                    total_documents=len(doc_manifests),
                    total_assets=total_assets,
                    total_attachments=0
                ),
                documents=doc_manifests
            )
            
            manifest_file = temp_path / "manifest.json"
            async with aiofiles.open(manifest_file, 'w', encoding='utf-8') as f:
                await f.write(manifest.model_dump_json(indent=2))
            
            # Create ZIP package
            package_path = temp_path / "documents.gpnu"
            with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add manifest
                zip_file.write(manifest_file, "manifest.json")
                
                # Add content files
                for content_file in content_dir.rglob("*"):
                    if content_file.is_file():
                        arcname = content_file.relative_to(temp_path)
                        zip_file.write(content_file, str(arcname))
                
                # Add assets
                for asset_file in assets_dir.rglob("*"):
                    if asset_file.is_file():
                        arcname = asset_file.relative_to(temp_path)
                        zip_file.write(asset_file, str(arcname))
            
            return package_path
            
        except Exception as e:
            logger.error(f"Export error: {e}")
            raise

