"""add_documents_table

Revision ID: add_documents_table
Revises: e33bb845793c
Create Date: 2025-01-20 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_documents_table'
down_revision: Union[str, None] = 'e33bb845793c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create documents table
    # Use String for UUID in SQLite, UUID in PostgreSQL
    id_type = postgresql.UUID(as_uuid=True) if op.get_bind().dialect.name == 'postgresql' else sa.String(36)
    
    op.create_table(
        'documents',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('content_summary', sa.Text(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('published', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('tags', sa.JSON(), default=list),
        sa.Column('relations', sa.JSON(), default=list),
        sa.Column('extra_metadata', sa.JSON(), default=dict),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)
    op.create_index(op.f('ix_documents_slug'), 'documents', ['slug'], unique=True)
    op.create_index(op.f('ix_documents_category'), 'documents', ['category'], unique=False)
    op.create_index(op.f('ix_documents_published'), 'documents', ['published'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_documents_published'), table_name='documents')
    op.drop_index(op.f('ix_documents_category'), table_name='documents')
    op.drop_index(op.f('ix_documents_slug'), table_name='documents')
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents')

