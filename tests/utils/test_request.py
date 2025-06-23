from typing import Any


class TestRequest:
    headers: dict

    def __init__(self, headers: dict):
        self.headers = headers


def test_context(auth_token: str) -> dict[str, Any]:
    return {"request": TestRequest({"authorisation": auth_token})}
