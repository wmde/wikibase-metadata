"""Wikibase User Type Enum"""

import enum

import strawberry


@strawberry.enum
class WikibaseUserType(enum.Enum):
    """Wikibase User Type"""

    BOT = 1
    MISSING = 2
    USER = 3
    NONE = 4
