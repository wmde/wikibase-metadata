"""Mock HTTP Response"""


class MockResponse:
    """Mock HTTP Response"""

    status_code: int
    content: bytes

    def __init__(self, status_code: int, content: bytes):
        self.content = content
        self.status_code = status_code
