---
name: 微信公众号文章爬虫
description: 使用 URL 提取微信公众号文章内容。
---

# 微信公众号文章爬虫技能

此技能允许您使用 URL 提取微信公众号文章的内容。

## 使用方法

该技能提供了一个 Python 脚本 `scripts/get_article.py`，它接受微信公众号文章 URL 作为参数，并输出文章的标题和内容预览。

### 命令

```bash
python3 scripts/get_article.py <URL>
```

### 示例

```bash
python3 scripts/get_article.py https://mp.weixin.qq.com/s/EwhrQgyZIVpk78IN8bNhFw
```

### 输出格式

输出将在控制台中打印文章的标题和内容预览。

### 依赖项

- python3
- requests
- beautifulsoup4

安装依赖项：

```bash
pip install requests beautifulsoup4
```
