---
name: Vesselfinder 船舶详情
description: 使用 IMO 编号从 Vesselfinder 提取特定船舶详情（名称、类型、旗帜、尺寸、吨位、航次信息、上一港口等）。
---

# Vesselfinder 船舶详情技能

此技能允许使用 IMO 编号从 Vesselfinder 提取有关船舶的详细信息。

## 使用方法

该技能提供了一个 Python 脚本 `scripts/get_ship_details.py`，它接受 IMO 编号作为参数，并以 JSON 格式输出船舶详情。

### 命令

```bash
python3 scripts/get_ship_details.py <IMO_NUMBER>
```

### 示例

```bash
python3 scripts/get_ship_details.py 9648714
```

### 输出格式

输出是一个 JSON 对象，**仅包含以下允许列表中的可用字段**：

- `imo`: 船舶的 IMO 编号。
- `name`: 船名。
- `vessel_type`: 船舶类型。
- `flag`: 船旗。
- `mmsi`: 水上移动通信业务标识码。
- `call_sign`: 呼号。
- `ais_type`: AIS 船舶类型。
- `gross_tonnage`: 总吨位。
- `summer_deadweight`: 夏季载重吨（吨）。
- `length_overall`: 总长（米）。
- `beam`: 船宽（米）。
- `year_of_built`: 建成年份。
- `destination`: 船舶报告的目的地。
- `eta`: 预计到达时间。
- `last_port`: 上一访问港口。
- `atd`: 实际出发时间。

**注意：** 空值、null 或受限字段（标记为 `-`）将从输出中省略。

### 依赖项

- python3
- requests
- beautifulsoup4

安装依赖项：

```bash
pip install requests beautifulsoup4
```
