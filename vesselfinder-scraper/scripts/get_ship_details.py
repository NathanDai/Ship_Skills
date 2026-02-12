import requests
from bs4 import BeautifulSoup
import argparse
import json
import sys


def get_ship_details(imo):
    url = f"https://www.vesselfinder.com/vessels/details/{imo}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    # 默认值
    ship_data = {
        "imo": imo,
        "name": None,
        "vessel_type": None,
        "flag": None,
        "gross_tonnage": None,
        "summer_deadweight": None,
        "length_overall": None,
        "beam": None,
        "year_of_built": None,
        "ais_type": None,
        "mmsi": None,
        "call_sign": None,
        "destination": None,
        "eta": None,
        "last_port": None,
        "atd": None,
    }

    # 提取名称
    title_section = soup.find("h1", class_="title")
    if title_section:
        ship_data["name"] = title_section.text.strip()

    # 如果 h1 中没找到名称，尝试在面包屑或其他地方查找
    if not ship_data["name"]:
        # 回退到页面标题
        if soup.title:
            title_text = soup.title.text
            # Title format: "SHIP NAME, Ship Type - Details and current position - IMO 1234567 - VesselFinder"
            parts = title_text.split(",")
            if parts:
                ship_data["name"] = parts[0].strip()

    # 提取航次数据（目的地、ETA、上一港口、ATD）
    voyage_rows = soup.find_all("div", class_="vi__r1")
    for row in voyage_rows:
        label_div = row.find("div", class_="vilabel")
        if not label_div:
            continue

        label_text = label_div.text.strip().lower()

        # 目的地 & ETA
        if "destination" in label_text:
            dest_elem = row.find("a", class_="_npNa")
            if dest_elem:
                ship_data["destination"] = dest_elem.text.strip()

            eta_elem = row.find("div", class_="_value")
            if eta_elem:
                eta_span = eta_elem.find("span", class_="_mcol12")
                if eta_span:
                    eta_text = eta_span.text.strip()
                    if eta_text.upper().startswith("ETA:"):
                        ship_data["eta"] = eta_text[4:].strip()
                    else:
                        ship_data["eta"] = eta_text

        # 上一港口 & ATD
        elif "last port" in label_text:
            port_elem = row.find("a", class_="_npNa")
            if port_elem:
                ship_data["last_port"] = port_elem.text.strip()

            atd_elem = row.find("div", class_="_value")
            if atd_elem:
                # 文本可能包含 "ATD: Feb 11, 03:28 UTC" 和一个类似 "(1 day ago)" 的 span
                # 我们只需要 span 之前的文本，或者去掉已知前缀的完整文本
                # 先获取完整文本
                full_atd_text = atd_elem.get_text(
                    " ", strip=True
                )  # "ATD: Feb 11, 03:28 UTC (1 day ago)"

                # 检查 "ATD:" 前缀
                if "ATD:" in full_atd_text:
                    # 简单解析：按 "ATD:" 分割并取第二部分
                    atd_val = full_atd_text.split("ATD:")[1].strip()
                    # 如果存在，移除括号中的相对时间，例如 "(1 day ago)"
                    if "(" in atd_val:
                        atd_val = atd_val.split("(")[0].strip()
                    ship_data["atd"] = atd_val

    # "船舶详细信息" 部分的解析器
    # 该部分通常包含一个带有键和值的表格
    # 根据观察，键通常在 'td.tpc1' 或类似元素中，值在 'td.txv' 或 'td.tpc2' 中
    # 使用通用方法查找表格行并将键映射到我们的字段

    technical_specs = {}

    # 查找所有表格和行
    rows = soup.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            key = cols[0].text.strip().lower().rstrip(":")
            value = cols[1].text.strip()
            technical_specs[key] = value

    # 将提取的规格映射到我们的 ship_data
    # 常见键: "imo / mmsi", "call sign", "flag", "gross tonnage", "summer deadweight (t)", "length overall (m) / beam (m)", "year of built", "vessel type"

    # 调试: 打印找到的键
    # print(f"Found keys: {list(technical_specs.keys())}", file=sys.stderr)

    # Vessel Type
    ship_data["vessel_type"] = technical_specs.get("ship type") or technical_specs.get(
        "vessel type"
    )

    # Flag
    ship_data["flag"] = technical_specs.get("flag")

    # MMSI & Call Sign
    # "imo / mmsi" -> "9333395 / 255806256"
    imo_mmsi = technical_specs.get("imo / mmsi")
    if imo_mmsi:
        parts = imo_mmsi.split("/")
        if len(parts) > 1:
            ship_data["mmsi"] = parts[1].strip()

    ship_data["call_sign"] = technical_specs.get("callsign") or technical_specs.get(
        "call sign"
    )

    # Gross Tonnage
    ship_data["gross_tonnage"] = technical_specs.get("gross tonnage")

    # Summer Deadweight
    ship_data["summer_deadweight"] = technical_specs.get(
        "deadweight (t)"
    ) or technical_specs.get("summer deadweight (t)")

    # Length Overall
    if "length overall (m)" in technical_specs:
        ship_data["length_overall"] = technical_specs.get("length overall (m)")
    elif "length overall (m) / beam (m)" in technical_specs:
        ship_data["length_overall"] = (
            technical_specs.get("length overall (m) / beam (m)").split("/")[0].strip()
        )

    # Beam
    if "beam (m)" in technical_specs:
        ship_data["beam"] = technical_specs.get("beam (m)")
    elif "length overall (m) / beam (m)" in technical_specs:
        parts = technical_specs.get("length overall (m) / beam (m)").split("/")
        if len(parts) > 1:
            ship_data["beam"] = parts[1].strip()

    # Year of Built
    ship_data["year_of_built"] = technical_specs.get(
        "year of build"
    ) or technical_specs.get("year of built")

    # AIS Info
    ship_data["ais_type"] = technical_specs.get("ais type")

    # 修正: IMO 通常是组合字段的一部分或单独存在。
    # 因为我们传递了 IMO，所以保留它。
    # 但我们可以验证 "imo / mmsi" 是否包含它。

    # Filter out empty, None, or restricted ("-") values and return
    # final_ship_data = {
    #     k: v
    #     for k, v in ship_data.items()
    #     if v is not None and v != "-" and (isinstance(v, str) and v.strip() != "" or not isinstance(v, str))
    # }

    # 用户请求严格的输出格式 + 航次数据
    allowed_keys = {
        "imo",
        "name",
        "vessel_type",
        "flag",
        "gross_tonnage",
        "summer_deadweight",
        "length_overall",
        "beam",
        "year_of_built",
        "ais_type",
        "mmsi",
        "call_sign",
        "destination",
        "eta",
        "last_port",
        "atd",
    }

    final_ship_data = {
        k: v
        for k, v in ship_data.items()
        if k in allowed_keys
        and v
        and v != "-"
        and (isinstance(v, str) and v.strip() != "" or not isinstance(v, str))
    }

    return final_ship_data


def main():
    parser = argparse.ArgumentParser(description="从 VesselFinder 获取船舶详情")
    parser.add_argument("imo", help="船舶的 IMO 编号")
    args = parser.parse_args()

    data = get_ship_details(args.imo)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
