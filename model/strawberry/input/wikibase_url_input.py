"""Wikibase URL Set - INPUT"""

from typing import Optional
import strawberry


@strawberry.input
class WikibaseURLSetInput:
    """Wikibase URL Set"""

    base_url: str

    action_api_url: Optional[str] = None

    index_api_url: Optional[str] = None

    sparql_query_url: Optional[str] = None

    sparql_endpoint_url: Optional[str] = None

    special_statistics_url: Optional[str] = None

    special_version_url: Optional[str] = None
