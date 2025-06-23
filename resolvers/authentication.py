"""Authentication"""

from starlette.requests import Request
from strawberry import Info
from strawberry.fastapi import BaseContext

from config import auth_token


def authenticate(info: Info[BaseContext]):
    """Authenticate"""

    authenticate_request(info.context['request'])



def authenticate_request(request: Request):
    """Authenticate Request"""

    print(request.headers.get("authorization", None))
    print(auth_token)
    assert request.headers.get("authorization", None) == auth_token, "Authorisation Failed"