from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class DocumentAuthor(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class DocumentRelation(BaseModel):
    type: str  # references, related, parent, child
    target_slug: str
    description: Optional[str] = None


class DocumentBase(BaseModel):
    slug: str
    title: str
    category: Optional[str] = None
    content_summary: Optional[str] = None
    published: bool = True
    tags: List[str] = []
    relations: List[DocumentRelation] = []
    extra_metadata: Dict[str, Any] = {}


class DocumentCreate(DocumentBase):
    file_path: Optional[str] = None
    author_id: Optional[int] = None


class DocumentUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    content_summary: Optional[str] = None
    published: Optional[bool] = None
    tags: Optional[List[str]] = None
    relations: Optional[List[DocumentRelation]] = None
    extra_metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(DocumentBase):
    id: UUID
    file_path: str
    author_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Package Manifest Schemas
class PackageExportedBy(BaseModel):
    user_id: int
    email: EmailStr
    username: str


class PackageInfo(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None


class PackageStatistics(BaseModel):
    total_documents: int
    total_assets: int = 0
    total_attachments: int = 0


class DocumentInManifest(BaseModel):
    id: UUID
    file_path: str
    slug: str
    title: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    authors: Optional[List[DocumentAuthor]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published: bool = True
    frontmatter: Optional[Dict[str, Any]] = None
    relations: Optional[List[DocumentRelation]] = None
    assets: Optional[List[str]] = None
    attachments: Optional[List[str]] = None
    
    @model_validator(mode='after')
    def ensure_lists_not_none(self):
        # Ensure list fields are never None - convert to empty lists
        if self.tags is None:
            object.__setattr__(self, 'tags', [])
        if self.authors is None:
            object.__setattr__(self, 'authors', [])
        if self.relations is None:
            object.__setattr__(self, 'relations', [])
        if self.assets is None:
            object.__setattr__(self, 'assets', [])
        if self.attachments is None:
            object.__setattr__(self, 'attachments', [])
        if self.frontmatter is None:
            object.__setattr__(self, 'frontmatter', {})
        return self


class DocumentPackageManifest(BaseModel):
    format_version: str
    format_spec: Optional[str] = None
    exported_at: datetime
    exported_by: PackageExportedBy
    package_info: Optional[PackageInfo] = None
    statistics: Optional[PackageStatistics] = None
    documents: List[DocumentInManifest]


class ImportOptions(BaseModel):
    conflict_strategy: str = "skip"  # skip, overwrite, rename
    import_assets: bool = True
    import_attachments: bool = True


class ImportResult(BaseModel):
    success: bool
    total: int
    imported: int
    skipped: int
    failed: int
    errors: List[str] = []

