import asyncio
import json
import argparse
import sys
from utils.api_client import get_article_html
from utils.formatters import parse_article
from utils.errors import WeChatParserError, InvalidURLError


async def main():
    parser = argparse.ArgumentParser(description="获取并解析微信文章。")
    parser.add_argument("url", help="微信文章的 URL。")
    args = parser.parse_args()

    # 验证 URL
    if not (
        args.url.startswith("http://mp.weixin.qq.com/s/")
        or args.url.startswith("https://mp.weixin.qq.com/s/")
    ):
        print(f"Error: {InvalidURLError().message}")
        print(f"Suggestion: {InvalidURLError().suggestion}")
        sys.exit(1)

    try:
        # 1. 获取 HTML 内容
        html_content = await get_article_html(args.url)

        # 2. 解析标题和内容
        title, content = parse_article(html_content)

        # 3. 格式化响应
        response_data = {"title": title, "content": content}

        # 输出 JSON 到标准输出
        print(json.dumps(response_data, ensure_ascii=False, indent=2))

    except WeChatParserError as e:
        print(f"Error: {e}")
        if e.suggestion:
            print(f"Suggestion: {e.suggestion}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
