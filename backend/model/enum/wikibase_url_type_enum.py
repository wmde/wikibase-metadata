"""Wikibase URL Type Enum"""

import enum


class WikibaseURLType(enum.Enum):
    """Wikibase URL Type"""

    BASE_URL = 1

    ACTION_QUERY_URL = 2
    """Deprecated"""

    ARTICLE_PATH = 8

    INDEX_QUERY_URL = 3
    """Deprecated"""

    SCRIPT_PATH = 9

    SPARQL_ENDPOINT_URL = 4

    SPARQL_FRONTEND_URL = 10

    SPARQL_QUERY_URL = 5
    """Deprecated"""

    SPECIAL_STATISTICS_URL = 6
    """Deprecated"""

    SPECIAL_VERSION_URL = 7
    """Deprecated"""
