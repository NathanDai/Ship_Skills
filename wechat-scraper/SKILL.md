---
name: WeChat Article Scraper
description: Extract content from WeChat articles using a URL.
---

# WeChat Article Scraper Skill

This skill allows you to extract content from WeChat articles using their URL.

## Usage

The skill provides a Python script `scripts/get_article.py` that takes a WeChat article URL as an argument and outputs the article's title and a preview of its content.

### Command

```bash
python3 scripts/get_article.py <URL>
```

### Example

```bash
python3 scripts/get_article.py https://mp.weixin.qq.com/s/EwhrQgyZIVpk78IN8bNhFw
```

### Output Format

The output will print the title of the article and a preview of the content to the console.

### Dependencies

- python3
- requests
- beautifulsoup4

To install dependencies:

```bash
pip install requests beautifulsoup4
```
