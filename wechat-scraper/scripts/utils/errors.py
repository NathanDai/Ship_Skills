class WeChatParserError(Exception):
    """Base exception for WeChat parser errors."""

    def __init__(self, message: str, suggestion: str = None):
        super().__init__(message)
        self.suggestion = suggestion


class RequestFailedError(WeChatParserError):
    """Raised when the HTTP request fails."""

    def __init__(self, status_code: int):
        super().__init__(
            message=f"Failed to fetch article (Status: {status_code})",
            suggestion="Check your network connection or if the URL is accessible.",
        )


class ParsingFailedError(WeChatParserError):
    """Raised when parsing the HTML fails."""

    def __init__(self):
        super().__init__(
            message="Failed to parse article content",
            suggestion="The article structure might have changed. Please check the selector.",
        )


class InvalidURLError(WeChatParserError):
    """Raised when the URL is invalid."""

    def __init__(self):
        super().__init__(
            message="Invalid WeChat article URL",
            suggestion="Please ensure the URL starts with https://mp.weixin.qq.com/s/",
        )
