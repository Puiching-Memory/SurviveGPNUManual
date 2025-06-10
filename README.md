# SurviveGPNUManual

广师大生存手册

[https://puiching-memory.github.io/SurviveGPNUManual/](https://puiching-memory.github.io/SurviveGPNUManual/)

## 页面部署

仅部署github pages，因为：  
gitee pages已下线，gitcode pages仅为企业用户开放，gitlab为国内代理模式（它有正经入口吗？）

## 开发环境

使用conda管理虚拟环境

```bash
conda create -n gpnu python=3.13
conda activate gpnu
pip install -r requirements.txt
```

启动调试服务器

```bash
mkdocs serve
mkdocs serve -a 0.0.0.0:80 --no-livereload
```

添加Github token到环境变量(可选)
如果你遇到此类错误，则必须考虑：
```bash
WARNING -  git-committers plugin may require a GitHub token if you exceed the API rate limit or for private repositories. Set it under 'token' mkdocs.yml config or MKDOCS_GIT_COMMITTERS_APIKEY environment variable.
```

1. MKDOCS_GIT_COMMITTERS_APIKEY
2. GITHUB_TOKEN

example:
```shell
powershell $env:GITHUB_TOKEN = "your_token_here"
cmd set GITHUB_TOKEN=your_token_here

powershell $env:MKDOCS_GIT_COMMITTERS_APIKEY = "your_token_here"
cmd set MKDOCS_GIT_COMMITTERS_APIKEY=your_token_here
```

推荐使用等宽字体，如[Maple Mono](https://github.com/subframe7536/maple-font)

## vega-lite图表

在线编辑器：https://vega.github.io/editor/?#/examples/vega-lite/line_monotone

## 致谢

@梦归云帆 @L1NINE @mybear123 @光钻 @eisofia @林登徒 @Dimo @我可以 @猫的双月术 @小小登下士