import argparse
import json
import requests
import sys


URL_BASE = "http://172.16.28.22:3000/rest/"


def fetch_wechat_history(mp_name: str, title: str, page: int, page_size: int):
    """
    Fetch WeChat articles history from the internal API.
    """
    url = f"{URL_BASE}wechat_basic/get_articles_by_mp_name"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": "",
    }

    payload = {"mp_name": mp_name, "title": title, "page": page, "page_size": page_size}

    try:
        response = requests.post(
            url, headers=headers, json=payload, verify=False
        )  # --insecure equivalent
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch WeChat articles via internal API."
    )
    parser.add_argument(
        "--mp_name",
        required=True,
        help="WeChat Official Account Name (e.g. '世纪环海Pansea')",
    )
    parser.add_argument(
        "--title", required=True, help="Article Title Keyword (e.g. '交易')"
    )
    parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    parser.add_argument(
        "--page_size", type=int, default=20, help="Page size (default: 20)"
    )

    args = parser.parse_args()

    data = fetch_wechat_history(args.mp_name, args.title, args.page, args.page_size)

    if data.get("code") == 0 and "data" in data and "items" in data["data"]:
        filtered_items = []
        for item in data["data"]["items"]:
            filtered_items.append(
                {
                    "time": item.get("time"),
                    "url": item.get("url"),
                    "title": item.get("title"),
                }
            )

        result = {
            "total": data["data"].get("total"),
            "page": data["data"].get("page"),
            "page_size": data["data"].get("page_size"),
            "page_count": data["data"].get("page_count"),
            "items": filtered_items,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
