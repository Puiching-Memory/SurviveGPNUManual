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


