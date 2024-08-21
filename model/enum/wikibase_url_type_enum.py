"""Wikibase URL Type Enum"""

import enum


class WikibaseURLType(enum.Enum):
    """Wikibase URL Type"""

    BASE_URL = 1
    ACTION_QUERY_URL = 2
    INDEX_QUERY_URL = 3
    SPARQL_ENDPOINT_URL = 4
    SPARQL_QUERY_URL = 5
    SPECIAL_STATISTICS_URL = 6
    SPECIAL_VERSION_URL = 7
