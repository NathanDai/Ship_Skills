import requests
from bs4 import BeautifulSoup
import sys
import json


def get_wechat_article_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    html = requests.get(url, headers=headers, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_article.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        soup = get_wechat_article_soup(url)
        title_tag = soup.find("h1", class_="rich_media_title")
        content_tag = soup.find("div", class_="rich_media_content")

        result = {
            "title": title_tag.get_text().strip() if title_tag else None,
            "content": content_tag.get_text().strip() if content_tag else None,
        }

        print(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        print(f"Error fetching article: {e}")


if __name__ == "__main__":
    main()
