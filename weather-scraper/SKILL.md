---
name: 天气爬虫
description: 查询特定城市的当前天气
---

# 天气技能

此技能允许您查询指定城市的当前天气状况。

## 使用方法

您可以直接从命令行使用 Python 脚本。

### 先决条件

- Python 3.7+
- 安装 `httpx` 库 (`pip install httpx`)

### 命令

运行脚本，并将城市名称作为参数：

```bash
python3 scripts/get_weather.py <city_name>
```

**示例：**

```bash
python3 scripts/get_weather.py Beijing
```

## 输出

脚本返回一个类似 JSON 的字典，包含：
- 城市名称
- 温度 (°C)
- 天气描述
- 湿度
- 风速
