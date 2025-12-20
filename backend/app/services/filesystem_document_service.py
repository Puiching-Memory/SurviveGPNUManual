"""
文件系统文档服务

直接从文件系统读取 markdown 文件，不依赖数据库。
用于读取 storage/data/documents 目录下的文档（支持主题分类：guides/career/blog）。
"""

import aiofiles
from pathlib import Path
from typing import Optional, List, Dict
import frontmatter
from datetime import datetime, timezone
from slugify import slugify

from app.config import DOCUMENTS_DIR
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class FilesystemDocumentService:
    """文件系统文档服务"""
    
    def __init__(self, content_dir: Optional[Path] = None):
        """
        初始化服务
        
        Args:
            content_dir: 内容目录路径，默认为 DOCUMENTS_DIR
        """
        self.content_dir = content_dir or DOCUMENTS_DIR
    
    def _find_markdown_files(self, directory: Path) -> List[Path]:
        """查找所有 markdown 文件"""
        md_files = []
        if not directory.exists():
            return md_files
        
        for path in directory.rglob("*.md"):
            if path.is_file():
                md_files.append(path)
        return md_files
    
    def _generate_slug_from_path(self, file_path: Path) -> str:
        """从文件路径生成 slug"""
        relative = file_path.relative_to(self.content_dir)
        # 移除 .md 扩展名并转换为 slug
        slug = str(relative.with_suffix('')).replace('\\', '/')
        # 清理 slug
        slug = slugify(slug, separator='-')
        return slug
    
    def _extract_category_from_path(self, file_path: Path) -> Optional[str]:
        """从文件路径提取分类（主题）"""
        try:
            relative = file_path.relative_to(self.content_dir)
            # 获取第一个路径组件作为分类（如 guides, career, blog）
            parts = relative.parts
            if len(parts) > 1:
                # 排除文件名，取第一个目录名
                return parts[0]
            return None
        except ValueError:
            return None
    
    async def list_documents(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        published: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict]:
        """
        列出所有文档
        
        Args:
            category: 分类过滤
            tags: 标签过滤
            published: 是否发布过滤
            skip: 跳过数量
            limit: 返回数量限制
            
        Returns:
            文档列表
        """
        md_files = self._find_markdown_files(self.content_dir)
        documents = []
        
        for md_file in md_files:
            try:
                doc_info = await self.get_document_info(md_file)
                if doc_info:
                    # 应用过滤
                    if category and doc_info.get('category') != category:
                        continue
                    if published is not None and doc_info.get('published') != published:
                        continue
                    if tags:
                        doc_tags = doc_info.get('tags', [])
                        if not isinstance(doc_tags, list):
                            doc_tags = []
                        if not any(tag in doc_tags for tag in tags):
                            continue
                    
                    documents.append(doc_info)
            except Exception as e:
                logger.error(f"Error reading document {md_file}: {e}")
                continue
        
        # 按更新时间排序（最新的在前）
        documents.sort(
            key=lambda x: x.get('updated_at', '1970-01-01T00:00:00Z'),
            reverse=True
        )
        
        # 分页
        return documents[skip:skip + limit]
    
    async def get_document_info(self, file_path: Path) -> Optional[Dict]:
        """
        获取文档信息（不读取完整内容）
        
        Args:
            file_path: 文件路径
            
        Returns:
            文档信息字典
        """
        if not file_path.exists():
            return None
        
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            post = frontmatter.loads(content)
            
            # 生成 slug
            slug = post.metadata.get('slug') or self._generate_slug_from_path(file_path)
            
            # 获取文件修改时间（备用）
            file_stat = file_path.stat()
            file_mtime = datetime.fromtimestamp(file_stat.st_mtime, tz=timezone.utc).isoformat().replace('+00:00', 'Z')
            
            # 处理创建日期
            created_at = post.metadata.get('dateCreated') or post.metadata.get('date')
            if isinstance(created_at, datetime):
                created_at = created_at.isoformat().replace('+00:00', 'Z') if created_at.tzinfo else created_at.isoformat() + 'Z'
            elif isinstance(created_at, str):
                pass  # 已经是字符串
            else:
                # 使用文件修改时间
                created_at = file_mtime
            
            # 处理更新日期
            updated_at = post.metadata.get('date') or post.metadata.get('dateCreated')
            if isinstance(updated_at, datetime):
                updated_at = updated_at.isoformat().replace('+00:00', 'Z') if updated_at.tzinfo else updated_at.isoformat() + 'Z'
            elif isinstance(updated_at, str):
                pass  # 已经是字符串
            else:
                # 使用文件修改时间
                updated_at = file_mtime
            
            # 处理标签
            tags = post.metadata.get('tags') or []
            if not isinstance(tags, list):
                tags = []
            
            # 处理分类（优先使用 frontmatter，否则从路径提取）
            category = post.metadata.get('category')
            if not category:
                category = self._extract_category_from_path(file_path)
            
            return {
                'slug': slug,
                'file_path': str(file_path.relative_to(self.content_dir)),
                'title': post.metadata.get('title', file_path.stem),
                'category': category,
                'tags': tags,
                'description': post.metadata.get('description', ''),
                'published': post.metadata.get('published', True),
                'created_at': created_at,
                'updated_at': updated_at,
                'frontmatter': dict(post.metadata),
                'content_preview': post.content[:200] if post.content else ''  # 预览前200字符
            }
        except Exception as e:
            logger.error(f"Error parsing document {file_path}: {e}")
            return None
    
    async def get_by_slug(self, slug: str) -> Optional[Dict]:
        """
        根据 slug 获取文档
        
        Args:
            slug: 文档 slug
            
        Returns:
            文档信息字典（包含完整内容）
        """
        md_files = self._find_markdown_files(self.content_dir)
        
        for md_file in md_files:
            doc_info = await self.get_document_info(md_file)
            if doc_info and doc_info.get('slug') == slug:
                # 读取完整内容
                async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
                    content = await f.read()
                
                post = frontmatter.loads(content)
                doc_info['content'] = post.content
                return doc_info
        
        return None
    
    async def get_by_path(self, relative_path: str) -> Optional[Dict]:
        """
        根据相对路径获取文档
        
        Args:
            relative_path: 相对于 content_dir 的路径
            
        Returns:
            文档信息字典（包含完整内容）
        """
        file_path = self.content_dir / relative_path
        if not file_path.exists() or not file_path.is_file():
            return None
        
        doc_info = await self.get_document_info(file_path)
        if doc_info:
            # 读取完整内容
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            post = frontmatter.loads(content)
            doc_info['content'] = post.content
            return doc_info
        
        return None
    
    async def read_content(self, slug: str) -> Optional[str]:
        """
        读取文档内容
        
        Args:
            slug: 文档 slug
            
        Returns:
            文档内容（markdown 文本）
        """
        doc = await self.get_by_slug(slug)
        if doc:
            return doc.get('content')
        return None

