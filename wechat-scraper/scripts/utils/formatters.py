from bs4 import BeautifulSoup
from .errors import ParsingFailedError


def parse_article(html: str) -> tuple[str, str]:
    """
    解析微信文章的 HTML 以提取标题和内容。

    Args:
        html: 文章页面的 HTML 内容。

    Returns:
        包含文章标题和内容的元组。

    Raises:
        ParsingFailedError: 如果无法找到标题或内容。
    """
    soup = BeautifulSoup(html, "lxml")

    # 提取标题
    title_tag = soup.find("h1", id="activity-name")
    if not title_tag:
        title_tag = soup.find("h2", class_="rich_media_title")  # 旧版本的后备方案

    if not title_tag:
        raise ParsingFailedError()
    title = title_tag.get_text().strip()

    # 提取内容
    content_div = soup.find("div", id="js_content")
    if not content_div:
        raise ParsingFailedError()

    # 获取所有段落的文本
    paragraphs = content_div.find_all("p")
    content = "\n".join(p.get_text().strip() for p in paragraphs)

    return title, content
