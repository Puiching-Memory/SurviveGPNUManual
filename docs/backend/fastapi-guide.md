# 后端开发的 FastAPI 指南

本指南概述了在此项目中如何使用 FastAPI 以及后端开发的关键概念。

## 为什么选择 FastAPI？

FastAPI 是一个现代化的、高性能的 Web 框架，用于使用 Python 3.7+ 构建 API，基于标准 Python 类型提示。主要优势包括：

*   **高性能：** 与 NodeJS 和 Go 相当，这要归功于 Starlette 和 Pydantic。
*   **快速编码：** 将开发功能的速度提高约 200% 到 300%。
*   **更少的错误：** 减少约 40% 的人为错误（感谢类型提示）。
*   **直观：** 出色的编辑器支持。到处都有自动完成。减少调试时间。
*   **简单：** 设计为易于使用和学习。减少阅读文档的时间。
*   **简洁：** 最小化代码重复。从每个参数声明中获得多个功能。
*   **健壮：** 获得生产就绪的代码。具有自动交互式文档。
*   **基于标准：** 基于（并完全兼容）API 的开放标准：OpenAPI 和 JSON Schema。

## 后端项目结构

我们的后端组织以促进模块化和可维护性。典型结构（位于 `backend/app/`）可能如下所示：

```
backend/
├── app/
│   ├── config/           # 配置设置（来自 .env）
│   ├── db/               # 数据库模型和会话
│   ├── logs/           # 日志文件
│   ├── routes/           # API 路由和端点
│   ├── schemas/          # Pydantic 模式（数据验证）
│   ├── services/         # 业务逻辑服务
│   ├── utils/            # 工具函数和常量
│   └── main.py           # FastAPI 应用实例和主路由器
├── alembic/           # Alembic 迁移（如果使用 Alembic）
├── tests/                # 单元测试和集成测试
├── .env.example          # 环境变量示例
├── .gitignore
├── alembic.ini           # Alembic 配置（如果使用）
├── Dockerfile            # 用于容器化的 Dockerfile
├── pyproject.toml        # 用于 Poetry 的 pyproject.toml
├── README.md             # 本文件
└── requirements.txt      # 项目依赖 
```

## 定义端点

端点使用路径操作装饰器（`@router.get`、`@router.post` 等）在 `app/api/v1/endpoints/` 中的模块内的函数上定义。然后这些路由器在 `app/main.py` 中的主 FastAPI 应用实例中包含。

**示例（`app/api/v1/endpoints/items.py`）：**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api.v1 import deps # 假设 deps.py 用于 get_db

router = APIRouter()

@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(deps.get_db)):
    return crud.item.create(db=db, item=item)

@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(deps.get_db)):
    db_item = crud.item.get(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
```

## 使用 Pydantic 进行数据验证

Pydantic 广泛用于数据验证、序列化和设置管理。

*   **请求体：** 定义一个继承自 `BaseModel` 的 Pydantic 模型（模式）。FastAPI 将自动根据此模式验证传入的请求数据。
*   **响应模型：** 在路径操作装饰器中使用 `response_model` 参数来定义响应的模式。FastAPI 将过滤并序列化输出数据以匹配此模式。
*   **路径和查询参数：** 路径和查询参数的类型提示也会被验证。

**示例（`app/schemas/item.py`）：**
```python
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True # 或对于 Pydantic v2 使用 from_attributes = True
```

## 依赖注入

FastAPI 的依赖注入系统是一个强大的功能，用于：

*   **数据库会话：** 为路径操作函数提供数据库会话（例如，`db: Session = Depends(deps.get_db)`）。
*   **身份验证和授权：** 获取当前用户或验证安全范围（例如，`current_user: models.User = Depends(deps.get_current_active_user)`）。
*   **共享逻辑：** 复用通用逻辑或参数。

依赖项定义为函数（通常在 `app/api/v1/deps.py` 中），FastAPI 将调用这些函数。

## 异步操作（`async`/`await`）

FastAPI 支持使用 `async def` 的异步路径操作函数。这对于 I/O 绑定操作（如数据库调用或外部 API 请求）至关重要，以防止阻塞服务器。

```python
@router.get("/async-items/")
async def read_async_items():
    # 示例：await some_async_io_operation()
    return [{"name": "Async Item 1"}, {"name": "Async Item 2"}]
```
确保您的数据库驱动程序和其他 I/O 库支持 `async` 操作（例如，用于 PostgreSQL 的 `asyncpg` 与 SQLAlchemy）。

## 身份验证

此项目通常使用 JWT（JSON Web Tokens）进行身份验证。流程通常涉及：
1.  一个端点（例如，`/login/access-token`），用户在其中提交凭据。
2.  如果有效，服务器生成并返回访问令牌。
3.  客户端在后续对受保护端点的请求的 `Authorization` 标头中包含此令牌（例如，`Bearer <token>`）。
4.  依赖项（`get_current_user`）验证令牌并检索用户。

用于密码哈希和 JWT 管理的安全实用程序通常在 `app/core/security.py` 中。

## 自动 API 文档

FastAPI 根据您的代码、Pydantic 模型和 OpenAPI 模式自动生成交互式 API 文档。

*   **Swagger UI：** 可在 `/docs` 访问（例如，`http://localhost:8000/docs`）。
*   **ReDoc：** 可在 `/redoc` 访问（例如，`http://localhost:8000/redoc`）。

此文档对于前端开发人员和 API 使用者来说非常宝贵。

## 进一步阅读

*   [FastAPI 官方教程](https://fastapi.tiangolo.com/tutorial/)
*   [Pydantic 文档](https://docs.pydantic.dev/)
