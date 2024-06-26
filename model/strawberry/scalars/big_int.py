# pylint: disable=unnecessary-lambda

"""Big Int"""

from typing import Union
import strawberry


# This is needed because GraphQL does not support 64 bit integers
BigInt = strawberry.scalar(
    Union[int, str],  # type: ignore
    serialize=lambda v: int(v),
    parse_value=lambda v: str(v),
    description="BigInt field",
)
