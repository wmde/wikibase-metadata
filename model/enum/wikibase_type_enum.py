"""Wikibase Type Enum"""

import enum

import strawberry


@strawberry.enum
class WikibaseType(enum.Enum):
    """Wikibase Type"""

    SUITE = 0
    CLOUD = 1
    OTHER = 2
