from bs4 import BeautifulSoup
from .errors import ParsingFailedError


def parse_article(html: str) -> tuple[str, str]:
    """
    Parses the HTML of a WeChat article to extract the title and content.

    Args:
        html: The HTML content of the article page.

    Returns:
        A tuple containing the title and the content of the article.

    Raises:
        ParsingFailedError: If the title or content cannot be found.
    """
    soup = BeautifulSoup(html, "lxml")

    # Extract title
    title_tag = soup.find("h1", id="activity-name")
    if not title_tag:
        title_tag = soup.find(
            "h2", class_="rich_media_title"
        )  # Fallback for older versions

    if not title_tag:
        raise ParsingFailedError()
    title = title_tag.get_text().strip()

    # Extract content
    content_div = soup.find("div", id="js_content")
    if not content_div:
        raise ParsingFailedError()

    # Get all text from paragraphs
    paragraphs = content_div.find_all("p")
    content = "\n".join(p.get_text().strip() for p in paragraphs)

    return title, content
