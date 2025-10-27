"""Wikibase Filter - INPUT"""

from typing import Optional
from model.enum.wikibase_type_enum import WikibaseType
import strawberry


@strawberry.input
class WikibaseTypeInput:
    """Include or Exclude Wikibase Types"""

    exclude: Optional[list[WikibaseType]]


@strawberry.input
class WikibaseFilterInput:
    """Filter Wikibases"""

    wikibase_type: Optional[WikibaseTypeInput]
