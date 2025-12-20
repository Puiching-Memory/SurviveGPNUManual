# 初始项目设置

本指南将引导您在本地计算机上设置 FastAPI React Starter 项目。您可以选择推荐的基于 Docker 的设置、使用自动化脚本或手动设置过程。

## 先决条件

在开始之前，请确保已安装以下软件：

*   **Git：** 用于克隆仓库。([下载 Git](https://git-scm.com/downloads))
*   **Docker & Docker Compose (v2)：** 用于推荐的基于 Docker 的设置和运行自动化设置脚本。Windows 和 Mac 的 Docker Desktop 通常包括两者。([下载 Docker Desktop](https://www.docker.com/products/docker-desktop))
    *   对于 Linux，您需要安装 Docker Engine 和 Docker Compose 插件。
*   **Python (3.10+)：** 手动后端设置所需。([下载 Python](https://www.python.org/downloads/))
*   **Node.js (LTS 版本，例如 20.x) & npm：** 手动前端设置所需。npm 随 Node.js 一起包含。([下载 Node.js](https://nodejs.org/))

## 1. 克隆仓库

首先，将项目仓库克隆到本地计算机：

```bash
git clone https://github.com/raythurman2386/fastapi-react-starter.git
cd fastapi-react-starter
```

## 2. 环境配置

此项目使用 `.env` 文件来管理环境变量。

*   **对于 Docker 设置和自动化脚本：**
    在**项目根目录**（`fastapi-react-starter/.env`）创建 `.env` 文件。如果存在示例，可以复制它，或使用以下内容创建：

    ```env
    # 数据库配置（由 Docker Compose 使用）
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_NAME=fastapi_db
    ```
    *注意：自动化设置脚本（`setup.ps1`、`setup.sh`）将尝试从 `.env.example` 创建此文件（如果存在）。*

*   **对于手动后端设置：**
    在 `backend` 目录（`fastapi-react-starter/backend/.env`）创建 `.env` 文件：

    ```env
    # 数据库配置
    DB_NAME=fastapi_db
    DB_USER=your_db_user      # 您的 PostgreSQL 用户名
    DB_PASSWORD=your_db_password  # 您的 PostgreSQL 密码
    DB_HOST=localhost
    DB_PORT=5432

    # FastAPI 设置
    ENVIRONMENT=development
    CORS_ORIGINS=["http://localhost:5173"] # 用于 CORS 的前端 URL
    # SECRET_KEY=your_strong_secret_key_here # 生成强密钥
    # ALGORITHM=HS256
    # ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
    *确保更新数据库凭据并取消注释/设置 `SECRET_KEY`。*

*   **对于手动前端设置：**
    前端使用 Vite，它处理以 `VITE_` 为前缀的环境变量。主要需要的变量是 `VITE_API_URL` 以指向后端。
    在 `frontend` 目录（`fastapi-react-starter/frontend/.env`）创建 `.env` 文件：

    ```env
    VITE_API_URL=http://localhost:8000
    ```

## 3. 设置方法

选择以下方法之一来设置项目：

### 方法 A：使用 Docker（推荐）

这是让所有服务（后端、前端、数据库、文档）启动并运行的最简单方法。

1.  确保 Docker Desktop（或 Linux 上的 Docker Engine + Compose 插件）正在运行。
2.  确保根 `.env` 文件已按上述说明配置。
3.  从项目根目录运行：

    ```bash
    docker compose up --build
    ```
    要在分离模式下运行（在后台），添加 `-d` 标志：
    ```bash
    docker compose up --build -d
    ```

    此命令将：
    *   为后端、前端和文档服务构建 Docker 镜像。
    *   启动 PostgreSQL、后端、前端和文档的容器。
    *   后端将在启动时自动应用数据库迁移。

### 方法 B：自动化设置脚本

项目包含脚本以帮助自动化初始 Docker 环境设置（检查依赖项并创建根 `.env` 文件）。

*   **对于 Windows：**
    1.  以管理员身份打开 PowerShell。
    2.  导航到项目根目录。
    3.  运行脚本：
        ```powershell
        .\setup.ps1
        ```
        脚本将检查 Docker Desktop，如果未找到，将尝试通过 `winget` 安装它。如果可用，它还将从 `.env.example` 创建根 `.env` 文件。

*   **对于 Linux/Mac：**
    1.  打开终端。
    2.  导航到项目根目录。
    3.  使脚本可执行并运行它：
        ```bash
        chmod +x setup.sh
        ./setup.sh
        ```
        脚本将检查 Docker，如果未找到，将尝试使用官方便捷脚本安装它。它还创建根 `.env` 文件。

    运行脚本后，按照方法 A 中的 Docker Compose 命令进行：
    ```bash
    docker compose up --build -d
    ```

### 方法 C：手动设置

如果您更喜欢在主机上直接运行后端和前端服务而不使用 Docker，请按照以下步骤操作。

1.  **后端设置：**
    *   **安装 PostgreSQL：** 在本地安装 PostgreSQL 并确保它正在运行。创建数据库（例如，`fastapi_db`）和具有此数据库权限的用户。
    *   **配置 `backend/.env`：** 按照"环境配置"部分中的说明创建和配置 `fastapi-react-starter/backend/.env`，确保数据库凭据与本地 PostgreSQL 设置匹配。
    *   **安装 Python 依赖：**
        ```bash
        cd backend
        python -m venv venv  # 创建虚拟环境（可选但推荐）
        source venv/bin/activate  # Windows: venv\Scripts\activate
        pip install -r requirements.txt
        ```
    *   **运行数据库迁移：**
        ```bash
        python manage.py migrate
        ```
    *   **运行后端服务器：**
        ```bash
        uvicorn app.main:app --reload --port 8000
        ```

2.  **前端设置：**
    *   **配置 `frontend/.env`：** 按照"环境配置"部分中的说明创建 `fastapi-react-starter/frontend/.env`，确保 `VITE_API_URL` 指向您手动运行的后端（例如，`http://localhost:8000`）。
    *   **安装 Node.js 依赖：**
        ```bash
        cd frontend
        npm install
        ```
    *   **运行前端开发服务器：**
        ```bash
        npm run dev
        ```
        这通常会在 `http://localhost:5173` 启动前端。

## 4. 访问应用程序

设置完成且服务运行后：

*   **前端应用程序：** [http://localhost:5173](http://localhost:5173)
*   **后端 API (Swagger UI)：** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **项目文档（如果使用 Docker/docs 服务）：** [http://localhost:8001](http://localhost:8001)

## 下一步

*   探索**[开发指南](development.md)**以获取有关项目结构、编码标准和常见开发任务的信息。
*   如果您计划为您的项目自定义此启动模板，请查看**[使其成为您的](make_it_yours.md)**。
