"""Wikibase - INPUT"""

from typing import Optional
import strawberry

from model.enum import WikibaseCategory, WikibaseType
from model.strawberry.input.wikibase_url_input import WikibaseURLSetInput


@strawberry.input
class WikibaseInput:
    """Wikibase"""

    wikibase_name: str

    organization: Optional[str] = None

    description: Optional[str] = None

    country: Optional[str] = None

    region: Optional[str] = None

    category: Optional[WikibaseCategory] = None

    test: Optional[bool] = False

    reuse: Optional[bool] = False

    urls: WikibaseURLSetInput

    wikibase_type: Optional[WikibaseType] = None
