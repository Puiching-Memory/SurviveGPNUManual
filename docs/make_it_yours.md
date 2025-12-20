# 使其成为您的：自定义启动模板

本指南帮助您采用 FastAPI React Starter 模板并将其适应为您自己的独特项目。

## 1. 介绍

FastAPI React Starter 旨在为您提供一个现代化的技术栈和合理的项目结构，让您有一个良好的开端。按照这些步骤重新命名和自定义它。

## 2. 重命名项目

一致的命名是关键。以下是更改项目名称的位置：

*   **根目录：**
    *   重命名主项目文件夹（例如，`fastapi-react-starter` 到 `my-awesome-project`）。
    *   如果您已经推送到 Git 远程，您可能需要更新远程 URL 或创建新仓库。

*   **后端（`backend/pyproject.toml`）：**
    *   更新 `[tool.poetry]` 下的 `name`：
        ```toml
        [tool.poetry]
        name = "my-awesome-project-backend"
        # ... 其他设置
        ```

*   **前端（`frontend/package.json`）：**
    *   更新 `name` 字段：
        ```json
        {
          "name": "my-awesome-project-frontend",
          // ... 其他设置
        }
        ```

*   **后端配置（`backend/app/config/config.py`）：**
    *   更改 `Settings` 类中的 `APP_NAME`：
        ```python
        class Settings(BaseSettings):
            APP_NAME: str = "My Awesome Project"
            # ... 其他设置
        ```

*   **文档（`docs/mkdocs.yml`）：**
    *   更新 `site_name`：
        ```yaml
        site_name: My Awesome Project Docs
        ```
    *   考虑添加/更新 `site_author` 和 `repo_url`：
        ```yaml
        site_author: Your Name or Organization
        repo_url: https://github.com/your-username/my-awesome-project
        site_url: https://docs.my-awesome-project.com # 如果您公开部署文档
        ```

*   **前端标题（`frontend/index.html`）：**
    *   更新 `<title>` 标签和 `<meta name="description">`：
        ```html
        <head>
            <meta charset="UTF-8" />
            <link rel="icon" type="image/x-icon" href="/favicon.ico" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <meta name="description" content="My Awesome Project 的描述。" />
            <title>My Awesome Project</title>
        </head>
        ```

## 3. 自定义后端 (FastAPI)

*   **核心逻辑：**
    *   审查并修改/删除 `backend/app/routes/` 中的现有示例路由（例如，`auth.py`、`health.py`）。
    *   更新或替换 `backend/app/schemas/` 中的模式。
    *   调整或删除 `backend/app/services/` 中的服务。
    *   在 `backend/app/db/models.py` 中定义您自己的 SQLAlchemy 模型并生成新迁移（参见[开发指南](development.md#database-migrations)）。
*   **配置（`backend/app/config/config.py`）：**
    *   **关键：** 为 JWT 身份验证设置新的强 `SECRET_KEY`（或 `JWT_SECRET_KEY` 环境变量）。不要使用开发默认值。
    *   为前端域名调整 `CORS_ORIGINS`。
    *   审查其他设置（数据库连接、API 前缀等）。
*   **依赖（`backend/requirements.txt` 或 `backend/pyproject.toml`）：**
    *   根据项目需求添加、删除或更新 Python 依赖。

## 4. 自定义前端 (React)

*   **核心逻辑和 UI：**
    *   审查并修改/删除 `frontend/src/components/` 和 `frontend/src/features/` 中的示例组件。
    *   更新 `frontend/src/App.tsx` 或 `frontend/src/routes/` 中的路由。
    *   调整或删除 `frontend/src/hooks/` 中的自定义钩子。
*   **样式（Tailwind CSS 和 shadcn/ui）：**
    *   修改 `frontend/tailwind.config.js` 以自定义 Tailwind 主题（颜色、字体等）。
    *   在 `frontend/src/index.css`（或等效文件）中调整全局样式。
    *   自定义或替换 `frontend/src/components/ui/` 中的 shadcn/ui 组件。
*   **公共资源：**
    *   用您自己的替换 `frontend/public/favicon.ico` 和其他图标/徽标。
    *   更新 `frontend/public/` 中的任何静态图像或资源。
*   **依赖（`frontend/package.json`）：**
    *   添加、删除或更新 Node.js 依赖。

## 5. Docker 配置（`docker-compose.yml`）

*   **容器名称：** 为了清晰，更新每个服务的 `container_name`：
    ```yaml
    services:
      postgres:
        container_name: myproject-db
        # ...
      backend:
        container_name: myproject-backend
        # ...
      frontend:
        container_name: myproject-frontend
        # ...
      docs:
        container_name: myproject-docs
        # ...
    ```
*   **镜像名称：** 如果您计划构建 Docker 镜像并将其推送到注册表，您需要在构建过程中适当地标记它们（例如，`your-registry/myproject-backend:latest`）。`docker-compose.yml` 中的 `build:` 上下文定义了如何在本地构建镜像。

## 6. 文档

*   **内容：** 使用项目概述更新 `docs/index.md`。
*   审查并修改 `docs/` 目录中的所有其他 `.md` 文件以反映项目的具体情况，删除或更改模板相关信息。
*   **配置（`docs/mkdocs.yml`）：** 如第 2 节所述，更新 `site_name`、`site_author`、`repo_url` 和 `site_url`。

## 7. 许可证

*   启动模板使用 MIT 许可证。如果您的项目需要不同的许可证，请更新项目根目录中的 `LICENSE` 文件。

## 8. 清理

*   搜索并删除任何模板特定的注释、`TODO` 项或不再相关的占位符代码。
*   删除或替换示例图像、SVG（如 `frontend/public/starter.svg`）和其他资源。
*   确保在部署到生产之前清除所有示例用户账户、数据或配置。

通过遵循这些步骤，您可以有效地将 FastAPI React Starter 模板转换为您自己应用程序的坚实基础。
