# 前端 (React + Vite)

此目录包含使用 React 和 Vite 构建的前端应用程序。

## 概述

- **框架**：React
- **构建工具**：Vite
- **样式**：Tailwind CSS v4、Shadcn UI
- **语言**：TypeScript

## 项目结构

```
frontend/
├── public/             # 静态资源
├── src/
│   ├── assets/         # 图片、字体等
│   ├── components/     # 可复用的 UI 组件
│   ├── context/        # 状态管理（例如，React Context）
│   ├── features/       # 基于功能的组件（例如，auth、dashboard）
│   ├── hooks/          # 自定义钩子
│   ├── layouts/        # 布局组件（例如，MainLayout）
│   ├── lib/            # 工具函数和常量
│   ├── pages/          # 页面组件（路由）
│   ├── routes/         # React Router 定义
│   ├── types/          # TypeScript 类型
│   ├── index.tsx       # 入口点
│   ├── index.css       # 全局样式
│   └── vite-env.d.ts   # Vite 环境类型
├── components.json     # Shadcn UI 配置
├── index.html          # 主 HTML 文件
├── package.json        # 项目依赖和脚本
├── README.md           # 本文件
├── tailwind.config.js  # Tailwind CSS 配置
├── tsconfig.json       # TypeScript 配置
├── Dockerfile          # 用于容器化的 Dockerfile
├── vite.config.ts      # Vite 配置
└── .gitignore          # Git 忽略文件
```
*（根据实际项目布局调整上述结构）*

## 开始使用

### 先决条件

- Node.js（推荐版本 22.10.0 或更高版本）
- npm 或 yarn

### 安装

1.  导航到 `frontend` 目录：
    ```bash
    cd frontend
    ```
2.  安装依赖：
    ```bash
    npm install
    # 或
    # yarn install
    ```

### 环境变量

通过复制 `.env.example`（如果存在）或手动创建，在 `frontend` 目录中创建 `.env` 文件。

关键环境变量：

- `VITE_API_URL`：后端 API 的基础 URL（例如，本地开发使用 `http://localhost:8000/api`，或您的生产 API URL）。

示例 `.env`：
```
VITE_API_URL=http://localhost:8000/api
```

### 可用脚本

在 `frontend` 目录中，您可以运行以下脚本：

- **`npm run dev` 或 `yarn dev`**：在开发模式下运行应用。在浏览器中打开 [http://localhost:5173](http://localhost:5173)（或 Vite 分配的端口）查看。如果您进行编辑，页面将重新加载。

- **`npm run build` 或 `yarn build`**：为生产构建应用到 `dist` 文件夹。它会在生产模式下正确打包 React 并优化构建以获得最佳性能。

- **`npm run lint` 或 `yarn lint`**：使用 ESLint 对代码库进行 lint 检查。

- **`npm run preview` 或 `yarn preview`**：在本地提供生产构建以预览它。

## 样式

此项目使用 Tailwind CSS 进行实用优先的样式设计。
- Tailwind 配置在 `tailwind.config.js` 中。
- 基础样式和自定义 CSS 可以在 `src/index.css` 中找到。

### Shadcn UI

此项目利用 [Shadcn UI](https://ui.shadcn.com/) 作为其组件库。Shadcn UI 不是传统的组件库；相反，您可以将单个组件安装到项目中，从而完全控制其代码和样式。

**添加新组件：**

要添加新的 Shadcn UI 组件，请使用 Shadcn UI CLI。确保您在 `frontend` 目录中：

```bash
npx shadcn-ui@latest add [component-name]
```
例如，要添加按钮：
```bash
npx shadcn-ui@latest add button
```
此命令会将组件的源代码添加到 `src/components/ui/`（或根据 `components.json` 中的配置）。

**配置：**

- Shadcn UI 配置在 `components.json` 中。
- 组件通常安装到 `src/components/ui`。

**自定义：**

由于您拥有组件代码，您可以通过编辑 `src/components/ui/` 中的文件直接自定义组件。使用 Tailwind CSS 实用类进行样式设计，使它们易于修改以适应项目的设计系统。

## 添加新组件和页面

- **组件**：在 `src/components/` 中创建新的可复用组件。
- **页面**：在 `src/pages/` 中创建新的页面组件，并确保将它们添加到路由配置中（例如，在 `App.tsx` 或专用路由文件中）。

## 更多信息

- [React 文档](https://reactjs.org/)
- [Vite 文档](https://vitejs.dev/)
- [Tailwind CSS 文档 (v4)](https://tailwindcss.com/docs)
- [Shadcn UI 文档](https://ui.shadcn.com/docs)
