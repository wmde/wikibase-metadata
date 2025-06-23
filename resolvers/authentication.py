"""Authentication"""

from starlette.requests import Request
from strawberry import Info
from strawberry.fastapi import BaseContext

from config import auth_token


def authenticate(info: Info[BaseContext]):
    """Authenticate"""

    assert info is not None
    assert info.context is not None
    assert 'request' in info.context
    assert info.context['request'] is not None

    authenticate_request(info.context["request"])


def authenticate_request(request: Request):
    """Authenticate Request"""

    assert (
        request.headers.get("authorization", None) == auth_token
    ), "Authorisation Failed"
