# 后端 (FastAPI)

此目录包含使用 FastAPI 构建的后端应用程序。

## 概述

- **框架**：FastAPI
- **语言**：Python（推荐版本 3.12）
- **数据库**：PostgreSQL（推荐版本 17）
- **身份验证**：JWT（JSON Web Tokens）

## 项目结构

```
backend/
├── app/
│   ├── config/           # 配置设置（来自 .env）
│   │   └── storage.py    # 存储目录结构配置
│   ├── db/               # 数据库模型和会话
│   ├── logs/             # 日志文件
│   ├── routes/           # API 路由和端点
│   ├── schemas/          # Pydantic 模式（数据验证）
│   ├── services/         # 业务逻辑服务
│   ├── utils/            # 工具函数和常量
│   └── main.py           # FastAPI 应用实例和主路由器
├── alembic/              # Alembic 迁移（如果使用 Alembic）
├── storage/              # 存储目录（文件系统存储）
│   ├── data/             # 数据文件（持久化存储）
│   │   ├── documents/    # 文档内容（主题分类：guides/career/blog）
│   │   ├── assets/       # 资源文件
│   │   ├── attachments/  # 附件
│   │   └── uploads/      # 用户上传文件
│   ├── cache/            # 缓存文件（可清理）
│   └── temp/             # 临时文件（定期清理）
├── tests/                # 单元测试和集成测试
├── .env.example          # 环境变量示例
├── .gitignore            # Git 忽略文件
├── alembic.ini           # Alembic 配置（如果使用）
├── Dockerfile            # 用于容器化的 Dockerfile
├── pyproject.toml         # 用于 Poetry 的 pyproject.toml
├── README.md             # 本文件
└── requirements.txt      # 项目依赖
```

## 开始使用

### 先决条件

- Python（推荐版本 3.12）
- Pip（Python 包安装程序）
- 正在运行的 PostgreSQL 实例（推荐版本 17）

### 安装和设置

1.  **导航到 `backend` 目录：**
    ```bash
    cd backend
    ```

2.  **创建并激活虚拟环境（使用 uv）：**
    ```bash
    # 使用 uv 创建虚拟环境（推荐）
    uv venv --python 3.13
    .venv\Scripts\activate  # Windows
    # 或
    source .venv/bin/activate  # Linux/Mac
    
    # 或者使用传统方式
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # Linux/Mac
    ```

3.  **安装依赖：**
    ```bash
    # 使用 uv（推荐，更快）
    uv pip install -r requirements.txt
    
    # 或使用 pip
    pip install -r requirements.txt
    ```

4.  **环境变量：**
    通过复制 `.env.example`（如果存在）或手动创建，在 `backend` 目录中创建 `.env` 文件。此文件将存储敏感配置，如果包含真实密钥，则不应提交到版本控制。

    关键环境变量：

    - `DATABASE_URL`：PostgreSQL 数据库的连接字符串（例如，`postgresql://user:password@host:port/dbname`）。
    - `SECRET_KEY`：用于签署 JWT 和其他安全用途的强且唯一的密钥。使用 `openssl rand -hex 32` 生成一个。
    - `ALGORITHM`：用于 JWT 的算法（例如，`HS256`）。
    - `ACCESS_TOKEN_EXPIRE_MINUTES`：访问令牌的过期时间。
    - `CORS_ORIGINS`：允许的 CORS 源列表，用逗号分隔（例如，`http://localhost:5173,https://yourdomain.com`）。

    示例 `.env`：
    ```env
    DATABASE_URL="postgresql://postgres:changethis@localhost:5432/appdb"
    SECRET_KEY="your_very_strong_secret_key_here"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
    ```

5.  **数据库迁移（使用 Alembic）：**
    此项目使用 Alembic 来管理数据库模式迁移。确保您的 `alembic.ini` 已配置，并且您的 `migrations/env.py` 正确指向您的 SQLAlchemy 模型的元数据。

    常用命令（从 `backend` 目录运行）：

    -   **生成新的迁移脚本（在模型更改后）：**
        ```bash
        alembic revision -m "your_descriptive_migration_message" --autogenerate
        ```
        *（始终仔细审查自动生成的脚本。）*
    -   **将所有待处理的迁移应用到数据库：**
        ```bash
        alembic upgrade head
        ```
    -   **查看迁移历史：**
        ```bash
        alembic history
        ```

    有关使用 Alembic 的综合指南，包括设置、编写迁移和最佳实践，请参阅[使用 Alembic 进行数据库迁移](../../docs/backend/alembic-migrations.md)文档。

### 运行开发服务器

## 关键 FastAPI 概念

此项目利用了 FastAPI 的几个强大功能：

*   **Pydantic 模型：** 用于数据验证、序列化和设置管理（参见 `app/schemas/`）。
*   **APIRouter：** 用于将应用程序结构化为多个可管理的模块（参见 `app/api/v1/endpoints/` 和 `app/api/api.py`）。
*   **依赖注入：** 广泛用于数据库会话、身份验证和其他共享逻辑（参见 `app/api/v1/deps.py`）。
*   **自动 API 文档：** 当开发服务器运行时，可在 `/docs` 访问交互式 Swagger UI，在 `/redoc` 访问 ReDoc。

有关在此项目中使用 FastAPI 的详细指南，包括创建端点、使用 Pydantic 和身份验证，请参阅[后端开发的 FastAPI 指南](../../docs/backend/fastapi-guide.md)。


安装依赖并配置 `.env` 文件后，您可以运行 FastAPI 开发服务器：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- `--reload`：在代码更改时启用自动重新加载。
- API 将在 `http://localhost:8000` 可访问。
- 交互式 API 文档（Swagger UI）将在 `http://localhost:8000/docs`。
- 替代 API 文档（ReDoc）将在 `http://localhost:8000/redoc`。

## 存储结构

项目使用文件系统存储，采用现代化的分层组织方式：

### 文档存储

文档按主题分类存储在 `storage/data/documents/` 目录下：

- **guides/**: 核心指南文档（手册主体）
  - `home.md` - 首页/序章
  - `daily.md` - 校园生活
  - `exam.md` - 学业指南
  - `tips.md` - 实用技巧
  - `data.md` - 数据资料
  - `community.md` - 社区指南

- **career/**: 职业与升学规划
  - `job.md` - 求职指南
  - `aspiration.md` - 升学规划
  - `postgraduate.md` - 读研指南
  - `after.md` - 毕业后指南

- **blog/**: 博客文章（个人分享和经验交流）

更多详情请参阅 [`storage/README.md`](./storage/README.md) 和 [`storage/data/documents/STRUCTURE.md`](./storage/data/documents/STRUCTURE.md)。

## API 结构

- API 端点在 `app/routes/` 中定义。
- 文件系统文档 API 在 `/api/filesystem-documents` 提供。
- 用于请求/响应验证的 Pydantic 模式在 `app/schemas/` 中。
- 数据库模型（SQLAlchemy）在 `app/db/models/` 中。
- 业务逻辑和 CRUD 操作在 `app/services/` 中。

## 测试

*（描述如何运行测试，例如，`pytest`）*

```bash
# 示例：pytest
pytest
```

## 更多信息

**项目特定指南：**

- [后端开发的 FastAPI 指南](../../docs/backend/fastapi-guide.md)
- [使用 Alembic 进行数据库迁移](../../docs/backend/alembic-migrations.md)

**官方文档：**

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
