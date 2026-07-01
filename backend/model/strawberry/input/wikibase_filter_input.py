"""Wikibase Filter - INPUT"""

from typing import Optional

import strawberry

from model.enum import WikibaseType


@strawberry.input
class WikibaseTypeInput:
    """Include or Exclude Wikibase Types"""

    exclude: Optional[list[WikibaseType]] = None
    include: Optional[list[WikibaseType]] = None


@strawberry.input
class WikibaseFilterInput:
    """Filter Wikibases"""

    ignore_reuse: Optional[bool] = None
    search_text: Optional[str] = None
    wikibase_type: Optional[WikibaseTypeInput] = None
