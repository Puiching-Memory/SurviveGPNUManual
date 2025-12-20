# AWS 部署配置

此目录包含使用 ECS 和 Fargate 将应用程序部署到 AWS 的示例配置。

### 文件：

- `buildspec.yml`：此文件由 AWS CodeBuild 使用，用于构建 Docker 镜像并将其推送到 Amazon ECR（Elastic Container Registry）。

- `task-definitions/`：此目录包含 ECS 任务定义模板。
  - `backend-task-def.json`：后端服务的任务定义。
  - `frontend-task-def.json`：前端服务的任务定义。

### 部署步骤：

1.  **创建 ECR 仓库**：创建两个 ECR 仓库，一个用于后端，一个用于前端。
2.  **设置 CodeBuild**：创建一个链接到源代码仓库的 CodeBuild 项目。使用此目录中的 `buildspec.yml` 作为构建规范。
3.  **创建 ECS 集群**：创建一个 ECS 集群来运行您的服务。
4.  **创建任务定义**：使用 `task-definitions` 目录中的 JSON 文件在 ECS 中注册新任务定义。您需要将占位符值（如 `YOUR_ECR_REPO_URI`）替换为实际的 ECR 仓库 URI。
5.  **创建 ECS 服务**：在 ECS 集群中创建两个服务，一个用于前端，一个用于后端，使用您刚创建的任务定义。使用负载均衡器配置它们以将其暴露到互联网。
