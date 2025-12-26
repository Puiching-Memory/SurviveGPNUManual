# 广师大生存手册

一个现代化的文档管理系统，包含 FastAPI 后端和 React 19 前端，使用 TypeScript、Tailwind CSS 和 shadcn/ui 组件。

![image](frontend/public/starter.svg)

## 功能特性

- **后端 (FastAPI)**

  - 快速且现代化的 Python Web 框架
  - 支持 PostgreSQL/SQLite 数据库，使用异步 SQLAlchemy ORM
  - 基于 JWT 的身份验证系统
  - 基于角色的访问控制
  - 异步数据库操作
  - 适当的连接池和清理
  - 使用 pydantic 进行环境配置
  - 结构化日志记录
  - 健康检查端点
  - 优雅的关闭处理
  - 模块化项目结构

- **前端 (React 19)**
  - 最新的 React 特性，包括 `use` 钩子
  - TypeScript 提供类型安全和更好的开发体验
  - React Router 7 用于客户端路由
  - shadcn/ui 组件提供美观、可访问的 UI
  - 基于组件的架构
  - 用于数据获取的自定义钩子
  - 使用 Error Boundaries 进行现代错误处理
  - 使用 Suspense 处理加载状态
  - Tailwind CSS 用于样式设计
  - 环境配置
  - Vite 提供快速开发体验

## 快速开始

### 使用 Docker（推荐）

1. 克隆仓库：

   ```bash
   git clone https://github.com/raythurman2386/fastapi-react-starter.git
   cd fastapi-react-starter
   ```

2. 创建环境文件：

   在根目录创建 `.env` 文件：

   ```env
   # 数据库配置
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=fastapi_db
   ```

3. 使用 Docker 启动应用：

   ```bash
   docker compose up --build
   ```

   这将：

   - 启动 PostgreSQL 数据库
   - 对新数据库应用迁移（例如，在删除 Docker 卷后）
   - 在 http://localhost:8000 启动 FastAPI 后端
   - 在 http://localhost:5173 启动 React 前端

   Swagger 文档可在 http://localhost:8000/docs 访问

### 自动化设置脚本

为了方便使用，本项目包含了适用于 Windows 和 Linux/Mac 的自动化设置脚本：

#### Windows 设置

1. 以管理员身份打开 PowerShell
2. 导航到项目目录
3. 运行设置脚本：
   ```powershell
   .\setup.ps1
   ```

此脚本将：

- 检查必需的依赖项（Docker、Docker Compose V2）
- 安装系统推荐的正确版本的 Docker
- 设置环境变量

#### Linux/Mac 设置

1. 打开终端
2. 导航到项目目录
3. 使脚本可执行并运行：
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

此脚本执行与 Windows 版本相同的设置步骤，但适用于基于 Unix 的系统。

### 创建管理员账号

在容器运行后，你可以通过以下命令创建管理员账号：

```bash
# 进入后端容器
docker compose exec backend python manage.py createsuperuser
```

这将提示你输入：
- 邮箱地址
- 用户名
- 密码（需要确认）

管理员账号创建后，可以使用该账号登录并访问管理功能。

### 数据库管理

项目包含多个数据库管理命令，需要在 Docker 容器内执行：

```bash
# 进入后端容器
docker compose exec backend python manage.py <command>

# 生成新迁移
docker compose exec backend python manage.py makemigrations "变更描述"

# 应用待处理的迁移
docker compose exec backend python manage.py migrate

# 检查迁移状态
docker compose exec backend python manage.py db-status

# 回滚最后一次迁移
docker compose exec backend python manage.py downgrade

# 创建管理员账号
docker compose exec backend python manage.py createsuperuser
```

如果遇到数据库错误并需要完全重置：

1. 停止所有运行的服务：`docker compose down`
2. 删除 PostgreSQL Docker 卷（例如，`docker volume rm fastapi-react-starter_postgres_data` - 使用 `docker volume ls` 验证卷名）
3. 重启服务：`docker compose up -d --build`

### 故障排除

1. 后端状态显示 "error"：

   - 确保 PostgreSQL 正在运行
   - 检查 `.env` 中的数据库凭据
   - 如需完全重置，请参阅上面的"如果遇到数据库错误"部分（涉及 Docker 卷删除）
   - 检查后端日志以获取具体错误消息

2. 用户注册失败：
   - 确保数据库已正确初始化
   - 检查后端是否正在运行且可访问
   - 验证后端 `.env` 中的 CORS 设置
   - 检查浏览器控制台以获取具体错误消息

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。
