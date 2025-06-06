"""Wikibase URL Set - INPUT"""

from typing import Optional
import strawberry


@strawberry.input
class WikibaseURLSetInput:
    """Wikibase URL Set"""

    base_url: str

    article_path: Optional[str] = None

    script_path: Optional[str] = None

    sparql_endpoint_url: Optional[str] = None

    sparql_frontend_url: Optional[str] = None
