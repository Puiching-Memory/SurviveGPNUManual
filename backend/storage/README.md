# Storage 目录结构

本目录包含应用程序的所有存储文件，采用现代化的分层组织方式。

## 目录结构

```
storage/
├── data/              # 数据文件（持久化存储）
│   ├── documents/     # 文档内容 (Markdown 文件)
│   ├── assets/        # 资源文件
│   │   ├── shared/    # 共享资源（所有文档共用的图片、文件等）
│   │   └── {doc_id}/  # 文档专属资源（按文档ID组织）
│   ├── attachments/   # 附件
│   └── uploads/       # 用户上传文件
├── cache/             # 缓存文件（可清理，不影响功能）
│   └── thumbnails/    # 缩略图缓存
└── temp/              # 临时文件（定期清理）
```

## 目录说明

### data/ - 数据文件目录

包含所有需要持久化存储的数据文件。这些文件是应用程序的核心数据，不应该被删除。

- **documents/**: 存储文档的 Markdown 文件，采用主题分类组织（guides/career/blog）
- **assets/**: 存储资源文件（图片、视频等）
  - **shared/**: 共享资源，所有文档都可以使用
  - **{doc_id}/**: 文档专属资源，按文档 UUID 组织
- **attachments/**: 附件文件
- **uploads/**: 用户上传的文件

### cache/ - 缓存目录

包含可以安全删除的缓存文件。删除这些文件不会影响应用程序功能，但可能会影响性能。

- **thumbnails/**: 图片缩略图缓存

### temp/ - 临时文件目录

包含临时文件，应该定期清理（例如：每天或每周）。

## 访问路径

- 共享资源: `/api/documents/assets/shared/{filename}`
- 文档资源: `/api/assets/{doc_id}/{filename}`
- 通用资源: `/api/assets/{path}`

## 注意事项

1. **不要手动删除 `data/` 目录下的文件**，除非你明确知道自己在做什么
2. **可以安全删除 `cache/` 目录**，应用程序会在需要时重新生成缓存
3. **定期清理 `temp/` 目录**，建议设置定时任务自动清理
4. **备份建议**: 定期备份 `data/` 目录，特别是 `documents/` 和 `assets/` 子目录

## 代码使用

在代码中使用存储目录：

```python
from app.config.storage import (
    DOCUMENTS_DIR,
    ASSETS_DIR,
    CACHE_DIR,
    TEMP_DIR,
    get_asset_dir,
    get_cache_path,
    get_temp_path,
    ensure_storage_directories,
)

# 确保目录存在（应用启动时调用）
ensure_storage_directories()

# 获取文档目录（支持主题分类）
doc_path = DOCUMENTS_DIR / "guides" / "home.md"  # 核心指南文档
doc_path = DOCUMENTS_DIR / "career" / "job.md"    # 职业规划文档
doc_path = DOCUMENTS_DIR / "blog" / "echo-01.md"  # 博客文章

# 获取资源目录
shared_assets = get_asset_dir()  # 共享资源
doc_assets = get_asset_dir(doc_id="uuid-here")  # 文档专属资源

# 获取缓存路径
cache_file = get_cache_path("thumbnails/image.jpg")

# 获取临时文件路径
temp_file = get_temp_path("upload-temp.pdf")
```

