"""MockRequest helper class"""

from typing import Any


class MockRequest:
    """MockRequest helper class"""

    headers: dict

    def __init__(self, headers: dict):
        self.headers = headers


def get_mock_context(auth_token: str) -> dict[str, Any]:
    """Return test context with provided token"""

    return {"request": MockRequest({"authorization": f"Bearer: {auth_token}"})}
