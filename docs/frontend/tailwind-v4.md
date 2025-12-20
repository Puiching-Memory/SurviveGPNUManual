# Tailwind CSS v4 集成

此项目利用 **Tailwind CSS v4**，这是实用优先 CSS 框架的最新版本。版本 4 在性能、新引擎和更简化的开发体验方面带来了重大改进，专为现代 Web 设计。

## 从 v3 的主要功能和更改

虽然可以在 [官方 Tailwind CSS v4 文档](https://tailwindcss.com/docs) 中找到更改的完整列表，但以下是与使用此模板的用户相关的一些亮点：

*   **新引擎 (Oxide)：** Tailwind CSS v4 具有用 Rust 编写的新高性能引擎，导致更快的构建时间和更响应的开发体验。
*   **简化的配置：** 配置文件（`tailwind.config.js` 或 `tailwind.config.ts`）可能看起来不同，采用更 CSS 优先的方法。许多常见的自定义现在更直观地处理。
*   **自动内容检测：** 在许多情况下，由于更智能的默认值，显式内容路径配置不太重要。
*   **第一方 Vite 插件：** 使用官方 `@tailwindcss/vite` 插件与 Vite 的集成更加顺畅。
*   **现代 CSS 功能：** v4 更原生地拥抱现代 CSS 功能，如级联层、容器查询和宽色域 P3 颜色。

## 现代浏览器要求

重要的是要注意，Tailwind CSS v4 专为现代浏览器环境设计。如果您需要支持旧浏览器，您可能考虑使用 Tailwind CSS v3.4 或实施适当的 polyfill。

Tailwind CSS v4 正式支持：

*   **Safari 16.4+**
*   **Chrome 111+**
*   **Firefox 128+**

确保您的目标受众与这些浏览器版本一致。

## 在此项目中使用 Tailwind CSS

*   **配置：** Tailwind CSS 配置位于 `frontend/tailwind.config.js`（或 `.ts`）。
*   **实用类：** 继续在 React 组件（TSX/JSX 文件）中直接使用 Tailwind 的实用类，就像您通常那样。
*   **基础样式：** 全局样式、自定义基础样式或组件层可以在 `frontend/src/index.css`（或您的主 CSS 入口点）中定义。

## 从 v3 升级（一般建议）

如果您之前使用 Tailwind CSS v3 并正在适应此 v4 模板，或者如果您正在升级另一个项目，请参考官方 [Tailwind CSS v4 升级指南](https://tailwindcss.com/docs/upgrade-guide)。

## 更多信息

有关最详细和最新的信息，请始终参考官方 [Tailwind CSS v4 文档](https://tailwindcss.com/docs)。
