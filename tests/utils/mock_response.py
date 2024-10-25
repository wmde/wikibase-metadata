"""Mock HTTP Response"""


class MockResponse:
    """Mock HTTP Response"""

    status_code: int
    content: bytes
    url: str

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __init__(self, url: str, status_code: int, content: bytes):
        self.url = url
        self.content = content
        self.status_code = status_code
