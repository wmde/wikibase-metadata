"""Wikibase - INPUT"""

from typing import Optional
import strawberry

from model.enum.wikibase_category_enum import WikibaseCategory
from model.strawberry.input.wikibase_url_input import WikibaseURLSetInput


@strawberry.input
class WikibaseInput:
    """Wikibase"""

    wikibase_name: str

    organization: Optional[str] = None

    description: str

    country: Optional[str] = None

    region: Optional[str] = None

    category: WikibaseCategory

    test: Optional[bool] = False

    urls: WikibaseURLSetInput
