# 部署指南

本指南提供了将 FastAPI React Starter 应用程序部署到生产环境的说明。主要描述的方法使用 Docker 和 Docker Compose。

## 1. 部署概述

部署此应用程序的推荐方法是使用 Docker Compose。此方法将后端、前端和数据库打包到可管理的服务中。

对于强大的生产设置，您通常会在应用程序前面放置反向代理（如 Nginx 或 Traefik）来处理 HTTPS、负载平衡，并可能更高效地提供静态前端资源。

## 2. 先决条件

*   **服务器：** 运行 Linux 发行版的服务器（VPS、专用服务器或云实例）。
*   **Docker & Docker Compose：** 确保在服务器上安装了 Docker 和 Docker Compose（v2 插件）。遵循官方安装指南。
*   **域名：** 指向服务器 IP 地址的注册域名。
*   **SSL 证书：** 用于启用 HTTPS 的域名的 SSL 证书（例如，来自 Let's Encrypt）。
*   **防火墙：** 配置服务器防火墙以允许必要端口上的流量（例如，80 用于 HTTP，443 用于 HTTPS）。

## 3. 生产配置

在部署之前，您**必须**为生产配置环境变量。强烈建议为生产使用单独的 `.env` 文件，或通过部署环境安全地管理这些变量。

### 3.1. 根 `.env` 文件（用于 Docker Compose）

在服务器上的项目根目录创建或更新 `.env` 文件：

```env
# 数据库配置（确保这些是强且唯一的凭据）
DB_USER=your_prod_db_user
DB_PASSWORD=your_prod_db_password
DB_NAME=your_prod_db_name

# 后端生产设置（在 docker-compose.yml 中传递给后端服务）
ENVIRONMENT=production
JWT_SECRET_KEY=generate_a_very_strong_random_secret_key # 重要！更改此值！
PROD_CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"] # 您的前端域名

# 前端生产设置（在 docker-compose.yml 中传递给前端服务）
PROD_VITE_API_URL=https://yourdomain.com/api # 您的后端 API 的 URL
```

**关键生产变量：**

*   `DB_USER`、`DB_PASSWORD`、`DB_NAME`：为生产数据库使用强且唯一的凭据。
*   `ENVIRONMENT=production`：将应用程序设置为在生产模式下运行（影响日志记录、错误处理等，如 `backend/app/config/config.py` 中定义）。
*   `JWT_SECRET_KEY`：**关键！** 此密钥用于签署 JWT。它**必须**是一个长、随机且保密的字符串。不要使用开发默认值。您可以使用 `openssl rand -hex 32` 生成一个。
*   `PROD_CORS_ORIGINS`：允许的 CORS 源的 JSON 格式字符串数组。将 `https://yourdomain.com` 替换为您实际的前端域名。
*   `PROD_VITE_API_URL`：您的后端 API 可访问的公共 URL（例如，如果通过反向代理在 `/api` 下提供）。

### 3.2. 用于生产的 Docker Compose 调整

最佳实践是为生产使用特定的 Docker Compose 文件（例如，`docker-compose.prod.yml`）或修改现有的 `docker-compose.yml` 以满足生产需求。以下是需要考虑的关键更改：

*   **删除开发卷：** 对于 `backend` 和 `frontend` 服务，删除将本地代码映射到容器中的主机挂载卷（例如，`volumes: - ./backend:/app`）。在生产中，代码应在构建过程中复制到镜像中。
*   **生产命令：**
    *   **后端：** 将 `command` 更改为使用生产级 ASGI 服务器，如带有 Uvicorn 工作器的 Gunicorn。示例：
        ```yaml
        # 在 docker-compose.yml 中用于后端服务
        command: gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app --bind 0.0.0.0:8000
        ```
        根据服务器的 CPU 核心数调整工作器数量（`-w 4`）。
    *   **前端：** `command` 应该提供构建的静态资源或运行生产 Node.js 服务器（如果适用）。如果您的 `frontend/Dockerfile` 构建静态资源（例如，到 `/app/dist`），您可能使用多阶段 Dockerfile 和轻量级 Web 服务器（如 Nginx）来提供这些文件。或者，如果 `npm run build` 创建 `dist` 文件夹，并且您的 `Dockerfile` 复制它并且 `npm start`（或 `package.json` 中的类似命令）使用生产就绪的静态服务器提供它，那也可以工作。
        *如果通过 Nginx（在前端容器中或单独的反向代理容器中）提供前端静态文件，`docker-compose.yml` 中的前端服务可能不需要直接暴露端口或可以简化。*
*   **环境变量：** 更新 `docker-compose.yml` 中 `backend` 和 `frontend` 服务的 `environment` 部分，以使用根 `.env` 文件中定义的生产值：
    ```yaml
    # backend 服务
    environment:
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=postgres # 保持为服务名称
      - DB_PORT=5432
      - CORS_ORIGINS=${PROD_CORS_ORIGINS}
      - ENVIRONMENT=${ENVIRONMENT:-production} # 默认为生产
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}      # 从根 .env 传递

    # frontend 服务
    environment:
      - VITE_API_URL=${PROD_VITE_API_URL} # 从根 .env 传递
      # 添加前端构建/运行时所需的任何其他生产环境变量
    ```
*   **端口：** 仅暴露需要外部访问的端口（通常通过反向代理，例如，端口 80 或 443）。内部服务到服务的通信使用 Docker 的内部网络。

**示例 `docker-compose.prod.yml`（说明性 - 与您的基础 `docker-compose.yml` 结合）：**

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    # 如果基础文件中存在，删除开发卷挂载
    # volumes: [] # 如果使用 extends，清除基础文件中的卷
    command: gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app --bind 0.0.0.0:8000
    environment:
      - ENVIRONMENT=production
      - CORS_ORIGINS=${PROD_CORS_ORIGINS}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    # 如果通过反向代理访问，可能删除端口映射
    # ports:
    #   - "8000:8000"

  frontend:
    # 删除开发卷挂载
    # volumes: []
    # command: npm run start # 或提供构建静态文件的命令
    environment:
      - VITE_API_URL=${PROD_VITE_API_URL}
    # 可能删除端口映射
    # ports:
    #  - "5173:5173"

# 确保 postgres_data 卷仍如基础 docker-compose.yml 中定义的那样定义
# volumes:
#   postgres_data:
```

要使用多个 compose 文件：`docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d`

## 4. 在生产中构建和运行

1.  **传输项目：** 将项目文件（包括生产就绪的 Dockerfile 和 Docker Compose 文件）复制到服务器。
2.  **创建 `.env` 文件：** 在服务器上创建根 `.env` 文件，其中包含上述生产值。
3.  **拉取最新镜像（可选但推荐）：**
    ```bash
    docker compose pull # 拉取基础镜像，如 postgres:17-alpine
    ```
4.  **构建并启动服务：**
    ```bash
    # 如果使用单个修改的 docker-compose.yml
    docker compose up --build -d

    # 如果使用 docker-compose.prod.yml 来覆盖/扩展
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
    ```
    `--build` 标志确保重建镜像。`-d` 标志在分离模式下运行服务。

5.  **数据库迁移：** 后端服务配置为 `command: bash -c "python manage.py run"`，它在内部在启动应用程序之前调用 `migrate`。如果您为生产更改此命令（例如，直接使用 Gunicorn），请确保迁移作为单独步骤运行，或作为容器入口点脚本的一部分在主应用程序启动之前运行。
    ```bash
    # 如果需要，手动运行迁移的示例
    docker compose exec backend python manage.py migrate
    ```

## 5. 数据持久性

`docker-compose.yml` 为 PostgreSQL 数据库定义了一个命名卷 `postgres_data`。这确保即使 `postgres` 容器停止或删除，您的数据库数据也会持久化。确保此卷作为服务器维护例程的一部分得到适当管理和备份。

## 6. 反向代理和 HTTPS（推荐）

对于生产，强烈建议使用反向代理，如 **Nginx** 或 **Traefik**。

**好处：**
*   **HTTPS/SSL 终止：** 处理 SSL 证书并加密流量。
*   **负载平衡：** （如果您扩展到多个后端实例）。
*   **提供静态文件：** Nginx 在提供静态前端资源方面非常高效。
*   **自定义域名：** 轻松将您的域名映射到应用程序。
*   **安全性：** 可以添加安全标头、速率限制等。

**使用 Nginx 的一般设置（概念性）：**
1.  在服务器上安装 Nginx。
2.  将 Nginx 配置为反向代理，将请求转发到您的容器化服务：
    *   对 `yourdomain.com/api/*` 的请求可以转到 `backend` 服务（例如，`http://localhost:8000`）。
    *   对 `yourdomain.com/*` 的请求可以提供静态前端资源（如果由 Nginx 构建和提供）或转到 `frontend` 服务（例如，`http://localhost:5173`）。
3.  在 Nginx 中为您的域名设置 SSL 证书（例如，使用 Certbot 和 Let's Encrypt）。

*有关详细配置说明，请参阅 Nginx 或 Traefik 文档。*

## 7. 部署文档 (MkDocs)

`docker-compose.yml` 中的 `docs` 服务提供文档。

1.  确保在运行 `docker compose up` 时包含 `docs` 服务。
2.  如果您有反向代理，配置它从子域（例如，`docs.yourdomain.com`）或路径（例如，`yourdomain.com/project-docs/`）路由流量到 `docs` 服务（例如，`http://localhost:8001`）。

或者，您可以将 MkDocs 站点构建为静态 HTML 文件，并将它们部署到任何静态托管提供商（例如，GitHub Pages、Netlify、AWS S3）：

```bash
# 从本地计算机，在项目根目录
docker compose run --rm docs mkdocs build
```
这将在 `docs/site/` 目录（或根据 `mkdocs.yml` 配置）中生成静态站点。然后您可以上传此 `site` 目录。

## 8. 监控和日志记录

*   **应用程序日志：** 使用 `docker compose logs backend` 和 `docker compose logs frontend` 查看应用程序日志。
*   **服务器监控：** 实施服务器级监控，用于 CPU、内存、磁盘空间和网络流量。
*   **日志聚合：** 对于更强大的日志记录，考虑设置集中式日志记录解决方案（例如，ELK 堆栈、Grafana Loki 或云提供商的日志记录服务）。

---

## 9. 云提供商部署

虽然 Docker Compose 非常适合单服务器部署，但您可能希望利用托管云平台（如 Google Cloud Run 或 AWS ECS）以获得更好的可扩展性、可靠性和更轻松的管理。

此项目中的 `deployments/` 目录包含这些平台的即用型配置文件。

### 9.1. Google Cloud Run

Google Cloud Run 是一个无服务器平台，可自动扩展您的容器化应用程序。

-   **配置文件：** `deployments/google-cloud/cloudbuild.yaml`
-   **方法：** 此文件与 Google Cloud Build 一起使用，自动构建后端和前端的 Docker 镜像，将它们推送到 Google Container Registry (GCR)，并将它们作为 Cloud Run 上的两个独立服务部署。

**部署：**
1.  **先决条件：**
    *   启用了计费的 Google Cloud 项目。
    *   安装并配置了 `gcloud` CLI。
    *   启用了 Cloud Build、Cloud Run 和 Container Registry API。
2.  **配置替换：** `cloudbuild.yaml` 使用替换变量（例如，`_REGION`、`_BACKEND_SERVICE_NAME`）。您可以直接在 Cloud Build 触发器或手动运行构建时设置这些。
3.  **设置触发器：** 在 Google Cloud Console 中，导航到 Cloud Build 并创建一个指向源代码仓库的触发器。配置它使用 `deployments/google-cloud/cloudbuild.yaml` 文件。
4.  **推送到部署：** 将提交推送到配置的分支将自动触发构建和部署过程。

*有关详细步骤，请参阅 [Google Cloud Run 文档](https://cloud.google.com/run/docs)。*

### 9.2. AWS Elastic Container Service (ECS) with Fargate

AWS ECS 是一个高度可扩展的容器编排服务。Fargate 是 ECS 的无服务器计算引擎，因此您无需管理服务器。

-   **配置文件：**
    -   `deployments/aws/buildspec.yml`：用于 AWS CodeBuild 构建镜像并推送到 ECR。
    -   `deployments/aws/task-definitions/`：包含后端和前端的 ECS 任务定义 JSON 模板。
-   **方法：**
    1.  **AWS CodePipeline：** 创建一个使用源代码仓库（例如，GitHub、AWS CodeCommit）的管道。
    2.  **构建阶段：** 添加一个使用 AWS CodeBuild 和 `buildspec.yml` 文件的构建阶段。这将构建您的 Docker 镜像并将它们推送到 Amazon ECR。
    3.  **部署阶段：** 添加一个使用"Amazon ECS"操作来使用任务定义部署服务的部署阶段。

**部署：**
1.  **先决条件：**
    *   AWS 账户。
    *   安装并配置了 `aws` CLI。
    *   用于后端和前端镜像的 ECR 仓库。
    *   ECS 集群。
2.  **自定义任务定义：** 更新 `*.json` 任务定义文件中的占位符值（例如，`<YOUR_BACKEND_ECR_REPO_URI>`、`<YOUR_AWS_ACCOUNT_ID>`）。
3.  **设置 CodePipeline：** 按照 AWS 文档创建从仓库到 ECS 集群自动化构建和部署过程的管道。

*有关详细步骤，请参阅 [AWS ECS 用户指南](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)。*


部署 Web 应用程序涉及许多考虑因素。本指南为自托管和两个顶级云提供商提供了一个起点。始终根据您的特定安全和性能要求调整配置。在您可以从此模板部署项目之前，您还有很长的路要走，一旦您达到可以部署项目的程度，请联系维护者寻求帮助。
