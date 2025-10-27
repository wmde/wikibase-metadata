"""Big Int"""

from typing import Union
import strawberry


# pylint: disable=unnecessary-lambda
BigInt = strawberry.scalar(
    Union[int, str],  # type: ignore
    serialize=lambda v: int(v),
    parse_value=lambda v: str(v),
    description="BigInt field",
)
"""GraphQL Does Not Support 64-bit Integers"""
