"""Authentication"""

from starlette.requests import Request
from strawberry import Info
from strawberry.fastapi import BaseContext

from config import auth_token


def authenticate(info: Info[BaseContext]):
    """Authenticate"""

    assert info is not None
    assert info.context is not None
    assert "request" in info.context
    assert info.context["request"] is not None

    authenticate_request(info.context["request"])


def authenticate_request(request: Request):
    """
    Authenticate Request
    Extract the token from an "Authorization: bearer <token>" header
    and check it against the configured authentication token.
    """

    auth_header_value = request.headers.get("authorization", None)
    if auth_header_value is None:
        raise ValueError("Authorization header missing")

    if not "bearer" in auth_header_value.lower():
        raise ValueError("Invalid authorization header, expected 'bearer'")

    auth_header_value_split = auth_header_value.split(" ")

    if len(auth_header_value_split) != 2:
        raise ValueError("Invalid authorization header, expected 'bearer <token>'")

    authenticate_token(auth_header_value_split[1])


def authenticate_token(token: str):
    """Authenticate Token"""

    assert token == auth_token, "Authorization Failed"
