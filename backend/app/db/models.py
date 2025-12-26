from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base
from passlib.context import CryptContext
import secrets
from uuid import uuid4


# Configure bcrypt context
# Use bcrypt with explicit configuration to avoid version detection issues
# Note: bcrypt 4.0.1 is used for compatibility with passlib 1.7.4
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b",  # Use bcrypt 2b identifier
    bcrypt__min_rounds=10,  # Minimum rounds for security
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # Roles: "user", "admin", "moderator"
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    reset_token = Column(String, unique=True, nullable=True)

    def verify_password(self, password: str) -> bool:
        """Check if a plain password matches the hashed password."""
        try:
            # Truncate password to 72 bytes if necessary (bcrypt limit)
            password_bytes = password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
                password = password_bytes.decode('utf-8', errors='ignore')
            return pwd_context.verify(password, self.hashed_password)
        except Exception:
            # Return False on any error to prevent information leakage
            return False

    def set_password(self, password: str):
        """Hash and store a password."""
        # Truncate password to 72 bytes if necessary (bcrypt limit)
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            password = password_bytes.decode('utf-8', errors='ignore')
        self.hashed_password = pwd_context.hash(password)

    def generate_reset_token(self):
        """Generate a secure reset token."""
        self.reset_token = secrets.token_urlsafe(32)

    def clear_reset_token(self):
        """Clear password reset token after use."""
        self.reset_token = None


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # content/{uuid}.md
    category = Column(String, nullable=True, index=True)
    content_summary = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    published = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 扩展字段
    tags = Column(JSON, default=list)  # 标签列表
    relations = Column(JSON, default=list)  # 关联关系
    extra_metadata = Column(JSON, default=dict)  # 扩展元数据（避免与SQLAlchemy的metadata冲突）
