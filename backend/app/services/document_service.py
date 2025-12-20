from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID, uuid4
from typing import Optional, List
from pathlib import Path
import aiofiles
import frontmatter
from slugify import slugify

from app.db.models import Document, User
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.config import DOCUMENTS_DIR
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, doc_id: UUID) -> Optional[Document]:
        """Get document by ID."""
        result = await self.db.execute(select(Document).filter(Document.id == doc_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Document]:
        """Get document by slug."""
        result = await self.db.execute(select(Document).filter(Document.slug == slug))
        return result.scalar_one_or_none()

    async def list_documents(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        published: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Document]:
        """List documents with filters."""
        query = select(Document)
        
        if category:
            query = query.filter(Document.category == category)
        if published is not None:
            query = query.filter(Document.published == published)
        if tags:
            # Filter by tags (JSON contains)
            for tag in tags:
                query = query.filter(Document.tags.contains([tag]))
        
        query = query.offset(skip).limit(limit).order_by(Document.updated_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_document(
        self,
        doc_data: DocumentCreate,
        author_id: Optional[int] = None
    ) -> Document:
        """Create a new document."""
        # Generate UUID if not provided
        doc_id = uuid4()
        
        # Generate file path
        if not doc_data.file_path:
            doc_data.file_path = f"content/{doc_id}.md"
        
        # Ensure slug is unique
        existing = await self.get_by_slug(doc_data.slug)
        if existing:
            raise ValueError(f"Document with slug '{doc_data.slug}' already exists")
        
        document = Document(
            id=doc_id,
            slug=doc_data.slug,
            title=doc_data.title,
            file_path=doc_data.file_path,
            category=doc_data.category,
            content_summary=doc_data.content_summary,
            author_id=author_id or doc_data.author_id,
            published=doc_data.published,
            tags=doc_data.tags,
            relations=doc_data.relations,
            extra_metadata=doc_data.extra_metadata
        )
        
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def update_document(
        self,
        doc_id: UUID,
        doc_data: DocumentUpdate
    ) -> Optional[Document]:
        """Update a document."""
        document = await self.get_by_id(doc_id)
        if not document:
            return None
        
        # Check slug uniqueness if slug is being updated
        if doc_data.slug and doc_data.slug != document.slug:
            existing = await self.get_by_slug(doc_data.slug)
            if existing and existing.id != doc_id:
                raise ValueError(f"Document with slug '{doc_data.slug}' already exists")
            document.slug = doc_data.slug
        
        if doc_data.title is not None:
            document.title = doc_data.title
        if doc_data.category is not None:
            document.category = doc_data.category
        if doc_data.content_summary is not None:
            document.content_summary = doc_data.content_summary
        if doc_data.published is not None:
            document.published = doc_data.published
        if doc_data.tags is not None:
            document.tags = doc_data.tags
        if doc_data.relations is not None:
            document.relations = doc_data.relations
        if doc_data.extra_metadata is not None:
            document.extra_metadata = doc_data.extra_metadata
        
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def delete_document(self, doc_id: UUID) -> bool:
        """Delete a document."""
        document = await self.get_by_id(doc_id)
        if not document:
            return False
        
        await self.db.delete(document)
        await self.db.commit()
        return True

    async def read_content(self, document: Document) -> str:
        """Read document content from file."""
        file_path = DOCUMENTS_DIR / document.file_path
        if not file_path.exists():
            raise FileNotFoundError(f"Document file not found: {file_path}")
        
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            return await f.read()

    async def write_content(self, document: Document, content: str) -> None:
        """Write document content to file."""
        file_path = DOCUMENTS_DIR / document.file_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)

    async def parse_markdown(self, content: str) -> tuple:
        """Parse markdown with frontmatter."""
        post = frontmatter.loads(content)
        return post.metadata, post.content

    def generate_slug(self, title: str) -> str:
        """Generate a URL-friendly slug from title."""
        return slugify(title)

