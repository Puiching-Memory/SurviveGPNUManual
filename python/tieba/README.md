## 开发环境

使用conda管理虚拟环境

```bash
conda create -n gpnu python=3.13
conda activate gpnu
pip install -r python/requirements.txt
```

```bash
scrapy crawl gpnu -o a_all.json
```