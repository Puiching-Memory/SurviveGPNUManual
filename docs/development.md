# 开发指南

本指南提供了在 FastAPI React Starter 项目中进行开发的说明和最佳实践。

## 1. 项目结构概述

项目组织为 `backend`（FastAPI）和 `frontend`（React）目录，以及用于本文档的 `docs` 目录和根级配置文件。

*   **`backend/`**：包含 FastAPI 应用程序。
    *   `app/`：核心应用程序代码（主应用、配置、数据库、路由、模式、服务、工具）。
    *   `requirements.txt`：Python 依赖。
    *   `pyproject.toml`：项目元数据和工具配置（例如，Black）。
    *   `manage.py`：用于数据库迁移和其他管理命令的脚本。
*   **`frontend/`**：包含 React 应用程序。
    *   `src/`：核心应用程序代码（组件、功能、钩子、布局等）。
    *   `package.json`：Node.js 依赖和脚本。
    *   `vite.config.ts`：Vite 构建配置。
    *   `tailwind.config.js`：Tailwind CSS 配置。
*   **`docs/`**：项目文档（MkDocs）。
*   **`docker-compose.yml`**：定义 Docker 的服务。
*   **`.pre-commit-config.yaml`**：预提交钩子的配置。

有关更详细的可视化结构，请参阅 `README.md` 或[项目概述](index.md)。

## 2. 后端开发 (FastAPI)

### 关键目录

*   **`app/main.py`**：FastAPI 应用程序入口点。
*   **`app/config/config.py`**：环境设置和日志配置。
*   **`app/db/`**：数据库连接（`database.py`）和 SQLAlchemy 模型（`models.py`）。
*   **`app/routes/`**：API 端点定义。
*   **`app/schemas/`**：用于数据验证和序列化的 Pydantic 模型。
*   **`app/services/`**：业务逻辑和服务层。
*   **`app/utils/`**：工具函数（例如，自定义日志设置，尽管主要日志记录在 `config.py` 中）。

### 代码检查和格式化

*   **Black**：使用 Black 强制执行代码格式化。配置在 `pyproject.toml` 中（`line-length = 100`）。
    *   建议将 Black 集成到您的 IDE 中，或在提交前手动运行它：
        ```bash
        # 导航到后端目录
        cd backend
        black .
        ```
*   **预提交钩子**：Black 也作为预提交钩子运行（参见下面的部分）。
*   **（可选）Ruff/Flake8/MyPy**：考虑添加 Ruff（用于代码检查和格式化，可以替代 Black/Flake8）或 MyPy（用于静态类型检查）以提高代码质量。将它们添加到 `requirements-dev.txt` 和 `.pre-commit-config.yaml`。

### 运行测试

此后端使用 pytest 和 coverage 设置。要运行测试，请导航到后端目录并运行：

```bash
cd backend
pytest
```

要运行带覆盖率的测试，请导航到后端目录并运行：

```bash
cd backend
pytest --cov=app
```

### 数据库迁移

项目使用 Alembic 进行数据库迁移，通过 `manage.py` 管理。

*   **生成新迁移（更改模型后）：**
    ```bash
    # 确保您在后端目录中
    cd backend
    python manage.py makemigrations "您的描述性迁移消息"
    ```
*   **应用迁移：**
    ```bash
    python manage.py migrate
    ```
*   **检查迁移状态：**
    ```bash
    python manage.py db-status
    ```
*   **降级（回滚）最后一次迁移：**
    ```bash
    python manage.py downgrade
    ```
*   **重置数据库（仅开发 - 删除所有表并重新应用所有迁移）：**
    ```bash
    python manage.py reset_db
    ```

### 日志记录

结构化日志记录在 `backend/app/config/config.py` 中配置。主应用程序记录器可以按以下方式导入和使用：

```python
from app.config import logger

logger.info("这是一条信息消息。")
logger.error("这是一条错误消息。")
```

### 添加新功能

1.  **模型（`app/db/models.py`）：** 定义或更新 SQLAlchemy 模型。
2.  **模式（`app/schemas/`）：** 创建用于请求/响应验证和序列化的 Pydantic 模式。
3.  **服务（`app/services/`）：** 实现业务逻辑。
4.  **路由（`app/routes/`）：** 定义新的 API 端点，使用服务和模式。
5.  **迁移：** 如果模型更改，生成并应用数据库迁移。
6.  **测试：** 为新功能编写测试。

## 3. 前端开发 (React)

### 关键目录

*   **`src/App.tsx`**：主 React 应用程序组件和路由器设置。
*   **`src/components/`**：可复用的 UI 组件。
    *   `ui/`：shadcn/ui 组件。
*   **`src/features/`**：特定功能模块（例如，auth、health）。
*   **`src/hooks/`**：自定义 React 钩子。
*   **`src/layouts/`**：页面布局组件。
*   **`src/lib/`**：工具函数和配置（例如，`utils.ts` 用于 shadcn）。
*   **`src/routes/`**：由 React Router 渲染的页面组件。
*   **`src/types/`**：TypeScript 类型定义。

### 代码检查、格式化和类型检查

*   **Prettier**：使用 Prettier 强制执行代码格式化。它配置为通过预提交钩子运行。
    *   要手动格式化：
        ```bash
        # 导航到前端目录
        cd frontend
        npm run format
        ```
    *   要检查格式化：
        ```bash
        npm run format:check
        ```
*   **ESLint**：（如果尚未由 Prettier/TypeScript 设置隐式处理，考虑添加 ESLint 以进行代码质量和样式规则）。
*   **TypeScript**：由 TypeScript 执行静态类型检查。
    *   要类型检查项目：
        ```bash
        # 导航到前端目录
        cd frontend
        npm run typecheck
        ```

### 运行测试

*（应在此处添加有关测试框架（例如，Vitest、React Testing Library）以及如何运行测试的文档。这将在将来添加前端测试时更新。）*

### 样式

*   **Tailwind CSS**：用于样式设计的实用优先 CSS 框架。配置在 `frontend/tailwind.config.js` 中。
*   **shadcn/ui**：使用 Radix UI 和 Tailwind CSS 构建的精美设计、可访问且可自定义的 React 组件集合。组件通常通过 shadcn/ui CLI 添加，可以在 `src/components/ui/` 中找到。

### 添加新功能/组件

1.  **定义类型（`src/types/`）：** 如果涉及新的数据结构。
2.  **创建组件（`src/components/` 或 `src/features/`）：** 开发新的 React 组件。
3.  **实现钩子（`src/hooks/`）：** 用于可复用逻辑或数据获取。
4.  **添加路由（`src/App.tsx` 或 `src/routes/`）：** 如果需要新页面。
5.  **样式：** 使用 Tailwind CSS 类和 shadcn/ui 组件。
6.  **测试：** 为新组件和逻辑编写测试。

## 4. 使用 Docker（开发）

在开发时，您可能需要与 Docker 容器交互：

*   **查看所有服务的日志：**
    ```bash
    docker compose logs -f
    ```
*   **查看特定服务的日志（例如，后端）：**
    ```bash
    docker compose logs -f backend
    ```
*   **访问运行中容器的 shell（例如，后端）：**
    ```bash
    docker compose exec backend /bin/bash
    ```
*   **重建并重启特定服务（例如，更改依赖后的后端）：**
    ```bash
    docker compose up --build -d backend
    ```
*   **停止所有服务：**
    ```bash
    docker compose down
    ```

## 5. 预提交钩子

项目使用由 `pre-commit` 管理的预提交钩子，在提交前自动检查和格式化代码。配置在 `.pre-commit-config.yaml` 中。

**钩子包括：**
*   `trailing-whitespace`：删除尾随空格。
*   `end-of-file-fixer`：确保文件以单个换行符结尾。
*   `check-yaml`：检查 YAML 文件的语法错误。
*   `check-added-large-files`：防止提交大文件。
*   `black`：格式化 Python 代码。
*   `prettier`：格式化前端代码（JS、TS、JSON、CSS、Markdown）。

**设置：**
如果您还没有，请安装 `pre-commit` 并设置钩子：

```bash
# 安装 pre-commit（如果尚未安装，例如，通过 pip 或 brew）
pip install pre-commit

# 从项目根目录安装 git 钩子脚本
pre-commit install
```
现在，钩子将在 `git commit` 时自动运行。

## 6. 调试技巧

*   **后端 (FastAPI)：**
    *   使用 `print()` 语句或配置的 `logger`。
    *   FastAPI 的交互式调试器（如果在开发模式下发生错误）。
    *   如果使用具有调试功能的 IDE（例如，VS Code），设置断点。
    *   如果通过 Docker 运行，检查 `docker compose logs backend` 以获取错误。
*   **前端 (React)：**
    *   使用浏览器开发工具（控制台、网络选项卡、React DevTools 扩展）。
    *   `console.log()` 语句。
    *   React DevTools 用于检查组件层次结构、状态和 props。
    *   如果通过 Docker 运行，检查 `docker compose logs frontend` 以获取构建错误。

---

本开发指南应该能帮助您开始。编码愉快！
