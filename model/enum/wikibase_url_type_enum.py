"""Wikibase URL Type Enum"""

import enum


class WikibaseURLType(enum.Enum):
    """Wikibase URL Type"""

    BASE_URL = 1
    ARTICLE_PATH = 2
    SCRIPT_PATH = 3
    SPARQL_ENDPOINT_URL = 4
    SPARQL_FRONTEND_URL = 5
