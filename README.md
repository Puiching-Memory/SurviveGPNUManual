# 广师大生存手册

一份由广师大学子共同维护的校园生活指南，使用 [Zensical](https://zensical.org/) 生成静态站点。

本仓库已移除原 FastAPI + React 前后端，只保留 `docs/` 目录下的手册正文，并改用 Zensical 直接生成静态站点。

## 目录结构

```
.
├── docs/              # 手册 Markdown 源文件
│   ├── index.md       # 站点首页
│   ├── guides/        # 核心指南
│   ├── career/        # 职业与升学
│   ├── blog/          # 博客文章
│   └── STRUCTURE.md   # 文档结构说明
├── zensical.toml      # Zensical 站点配置
└── README.md          # 本文件
```

## 本地预览

### 安装 Zensical

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install zensical
```

或使用 uv：

```bash
uv add --dev zensical
uv run zensical serve
```

### 启动预览服务器

```bash
zensical serve
```

默认访问 http://localhost:8000。

### 构建静态站点

```bash
zensical build
```

构建输出位于 `site/` 目录。

## 添加/修改内容

直接编辑 `docs/` 下的 Markdown 文件即可。新增页面后，若需调整导航顺序，修改 `zensical.toml` 中的 `nav` 配置。

## 部署

Zensical 生成的是纯静态文件，可将 `site/` 目录部署到任意静态托管服务，例如：

- GitHub Pages
- Cloudflare Pages
- Vercel / Netlify
- 自有 Nginx/CDN

## 贡献

欢迎提交 Pull Request 或发送邮件到 1138663075@qq.com。

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。
