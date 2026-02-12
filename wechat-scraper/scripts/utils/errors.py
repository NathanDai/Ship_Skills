class WeChatParserError(Exception):
    """微信解析器错误的基类。"""

    def __init__(self, message: str, suggestion: str = None):
        super().__init__(message)
        self.suggestion = suggestion


class RequestFailedError(WeChatParserError):
    """当 HTTP 请求失败时引发。"""

    def __init__(self, status_code: int):
        super().__init__(
            message=f"无法获取文章 (状态码: {status_code})",
            suggestion="请检查您的网络连接或 URL 是否可访问。",
        )


class ParsingFailedError(WeChatParserError):
    """当解析 HTML 失败时引发。"""

    def __init__(self):
        super().__init__(
            message="无法解析文章内容",
            suggestion="文章结构可能已更改。请检查选择器。",
        )


class InvalidURLError(WeChatParserError):
    """当 URL 无效时引发。"""

    def __init__(self):
        super().__init__(
            message="无效的微信文章 URL",
            suggestion="请确保 URL 以 https://mp.weixin.qq.com/s/ 开头",
        )
