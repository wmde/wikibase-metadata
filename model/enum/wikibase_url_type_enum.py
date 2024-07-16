"""Wikibase URL Type Enum"""

import enum


class WikibaseURLTypes(enum.Enum):
    """Wikibase URL Types"""

    BASE_URL = 1
    ACTION_QUERY_URL = 2
    INDEX_QUERY_URL = 3
    SPARQL_ENDPOINT_URL = 4
    SPARQL_QUERY_URL = 5
    SPECIAL_VERSION_URL = 6
