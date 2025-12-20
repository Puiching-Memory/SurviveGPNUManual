# Shadcn UI 指南

此项目利用 [Shadcn UI](https://ui.shadcn.com/) 来构建其用户界面。Shadcn UI 不是传统的组件库，而是一个精美设计的组件集合，您可以复制并粘贴到应用程序中。这种方法使您完全拥有和控制代码，允许深度自定义。

## 理念

理解 Shadcn UI 背后的理念是有效使用它的关键：

*   **您拥有代码：** 当您添加组件时，其源代码直接添加到您的项目中（通常在 `frontend/src/components/ui/` 下）。您可以根据需要修改它。
*   **不是依赖项：** 它不是您从 npm 以通常方式安装的包（除了 CLI 工具）。这意味着没有与第三方库的版本冲突，也不需要等待库维护者更新或修复某些内容。
*   **使用 Radix UI 和 Tailwind CSS 构建：** 组件通常使用 [Radix UI Primitives](https://www.radix-ui.com/) 构建以实现可访问性和行为，并使用 [Tailwind CSS](https://tailwindcss.com/) 进行样式设计，采用实用优先的方法。

## 添加组件

要将新组件添加到项目中，请使用 Shadcn UI CLI。确保您在 `frontend` 目录中：

```bash
npx shadcn-ui@latest add [component-name]
```

例如，要添加 `alert-dialog`：

```bash
npx shadcn-ui@latest add alert-dialog
```

此命令通常会执行以下操作：
1.  检查您的 `components.json` 以获取配置。
2.  为组件安装任何必要的依赖项（例如，`@radix-ui/react-alert-dialog`）。
3.  将组件的源代码添加到 `frontend/src/components/ui/`。

## 配置（`components.json`）

Shadcn UI CLI 的行为由位于 `frontend` 目录中的 `components.json` 文件配置。此文件定义：

*   `$schema`：`components.json` 的模式 URL。
*   `style`：要使用的组件样式（例如，"default"、"new-york"）。此模板使用 `default`。
*   `rsc`：是否安装 React Server Components (RSC) 兼容组件（true/false）。
*   `tsx`：是否为组件使用 TypeScript（true/false）。此模板使用 `true`。
*   `tailwind`：
    *   `config`：Tailwind CSS 配置文件路径。
    *   `css`：导入 Tailwind 指令的主 CSS 文件路径。
    *   `baseColor`：主题的基础颜色（例如，"slate"、"zinc"）。
    *   `cssVariables`：是否使用 CSS 变量进行主题设置。
*   `aliases`：
    *   `components`：存储 UI 组件的位置的路径别名（例如，`~/components`，可能映射到 `src/components`）。
    *   `utils`：工具函数的路径别名（例如，`~/lib/utils` 用于 `cn()` 函数）。

如果您偏离模板的默认值，请确保此文件针对您的项目结构正确配置。

## 自定义组件

由于组件代码直接在您的项目中（例如，`frontend/src/components/ui/button.tsx`），您可以通过以下方式自定义它：

*   **修改样式：** 直接在组件的 TSX 文件中更改 Tailwind CSS 类。
*   **更改行为：** 更改底层 Radix UI 原语或添加您自己的逻辑。
*   **扩展功能：** 向组件添加新的 props 或功能。

## 主题设置

Shadcn UI 组件设计为使用 CSS 变量进行主题设置。检查 `frontend/src/index.css`（或您的主 CSS 文件）以获取初始化 Shadcn UI 时定义的主题变量。您可以自定义这些变量以更改组件的整体外观和感觉。

## 最佳实践

*   **保持 CLI 更新：** 偶尔运行 `npx shadcn-ui@latest init` 以确保您的 CLI 和本地设置与 Shadcn UI 的任何更改保持最新（如果您大量自定义了 `components.json`，请小心并审查更改）。
*   **参考官方文档：** 对于特定组件的 API、props 和使用示例，始终参考 [官方 Shadcn UI 文档](https://ui.shadcn.com/docs/components/accordion)。
*   **了解依赖项：** 当您添加组件时，它可能会安装对等依赖项（如 Radix UI 包）。请注意 `package.json` 中的这些。

通过遵循本指南并利用官方文档，您可以有效地使用 Shadcn UI 为此应用程序构建美观且高度可自定义的前端。
