---
name: 微信公众号历史文章抓取
description: 使用 URL 提取微信公众号历史文章列表。
---

# 微信公众号历史文章抓取技能

此工具使用内部 API 获取微信公众号的历史文章列表。

### 用法

```bash
python3 scripts/get_history.py --mp_name "世纪环海Pansea" --title "交易" --page 1 --page_size 20
```

### 参数说明

- `--mp_name`: 微信公众号名称 (必填)
- `--title`: 文章标题关键词 (必填)
- `--page`: 页码 (默认: 1)
- `--page_size`: 每页数量 (默认: 20)

### 返回结果示例

返回一个包含分页元数据和文章列表的 JSON 对象：

```json
{
  "total": 508,
  "page": 1,
  "page_size": 20,
  "page_count": 26,
  "items": [
    {
      "time": "2026-02-11 13:21:48",
      "url": "https://mp.weixin.qq.com/s/n4XL4JP5tSHWPDvtKfm24g",
      "title": "[第6周] 船舶交易市场周报"
    },
    ...
  ]
}
```

### 依赖库

- `requests`
