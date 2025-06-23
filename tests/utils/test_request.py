"""TestRequest helper class"""

from typing import Any


class TestRequest:
    """Test Request helper class"""

    headers: dict

    def __init__(self, headers: dict):
        self.headers = headers


def get_test_context(auth_token: str) -> dict[str, Any]:
    """Return test context with provided token"""

    return {"request": TestRequest({"authorization": auth_token})}
