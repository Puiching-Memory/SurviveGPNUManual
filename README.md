# SurviveGPNUManual

广师大生存手册

[https://puiching-memory.github.io/SurviveGPNUManual/](https://puiching-memory.github.io/SurviveGPNUManual/)

## 是否能部署国内页面？目前无计划

gitee pages已下线，gitcode pages仅为企业用户开放，gitlab为国内代理模式（它有正经入口吗？）

## 开发环境

使用conda管理虚拟环境

```
conda create -n gpnu python=3.12
conda activate gpnu
pip install -r requirements.txt
```

启动调试服务器

```
mkdocs serve
```

添加Github token到环境变量(可选)

1. MKDOCS_GIT_COMMITTERS_APIKEY
2. GITHUB_TOKEN

example:
```
powershell $env:GITHUB_TOKEN = "your_token_here"
cmd set GITHUB_TOKEN=your_token_here
```

推荐使用等宽字体，如[Maple Mono]()

## 致谢
