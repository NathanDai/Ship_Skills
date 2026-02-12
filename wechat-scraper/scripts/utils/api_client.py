import httpx
from .errors import RequestFailedError

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"


async def get_article_html(url: str) -> str:
    """
    获取给定 URL 的 HTML 内容。

    Args:
        url: 微信文章的 URL。

    Returns:
        作为字符串的页面 HTML 内容。

    Raises:
        RequestFailedError: 如果 HTTP 请求失败。
    """
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url, headers=headers, follow_redirects=True, timeout=15.0
            )
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            raise RequestFailedError(status_code=e.response.status_code)
        except httpx.RequestError as e:
            # 传递 0 或适当的网络错误代码
            raise RequestFailedError(status_code=0) from e
