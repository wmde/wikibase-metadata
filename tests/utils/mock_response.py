"""Mock HTTP Response"""

from typing import Optional

from requests import HTTPError


class MockResponse:
    """Mock HTTP Response"""

    status_code: int
    content: bytes
    url: str

    def raise_for_status(self):
        """Raise Error if Status != 200"""

        if self.status_code is not None and self.status_code != 200:
            raise HTTPError

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __init__(self, url: str, status_code: int, content: Optional[bytes] = None):
        self.url = url
        self.content = content
        self.status_code = status_code
