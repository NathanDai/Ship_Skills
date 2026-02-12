---
name: 船舶搜索
description: 使用内部 API 通过船名搜索船舶详情。
---

# 船舶搜索技能

此技能允许你使用船名搜索船舶详情。

## 使用方法

该技能提供了一个 Python 脚本 `scripts/search_vessel.py`，它接受船名作为参数，并以 JSON 格式输出船舶详情。

### 命令

```bash
python3 scripts/search_vessel.py <VESSEL_NAME>
```

### 示例

```bash
python3 scripts/search_vessel.py "JETSTREAM"
```

### 输出格式

输出是一个 JSON 数组，包含多个可能匹配的船舶详情，每个对象包含以下字段：

- `vessel_name`: 船名
- `year_build`: 建成年份
- `imo`: IMO 编号
- `mmsi`: 水上移动通信业务标识码
- `vessel_type`: 船舶类型
- `flag`: 船旗
- `length_overall_m`: 总长（米）
- `beam_m`: 船宽（米）
- `gross_tonnage`: 总吨位
- `dwt`: 载重吨
- `builder`: 建造商
- `home_port`: 母港
- `former_names`: 曾用名

### 依赖项

- python3
- requests

安装依赖项：

```bash
pip install requests
```
