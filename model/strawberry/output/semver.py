"""Semantic Version"""

from typing import Optional
import strawberry


@strawberry.type
class Semver:
    """Semantic Version"""

    major: int
    minor: int
    patch: Optional[int]

    def __init__(self, major: int, minor: int, patch: Optional[int] = None):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
