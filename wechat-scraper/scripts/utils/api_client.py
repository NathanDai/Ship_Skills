import httpx
from .errors import RequestFailedError

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"


async def get_article_html(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url: The URL of the WeChat article.

    Returns:
        The HTML content of the page as a string.

    Raises:
        RequestFailedError: If the HTTP request fails.
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
            # Pass 0 or appropriate code for network errors
            raise RequestFailedError(status_code=0) from e
