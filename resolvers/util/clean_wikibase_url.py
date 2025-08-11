"""Clean Wikibase URL"""

import re

from model.enum import WikibaseURLType


FULL_URL_PATTERN = re.compile(r"https?://[A-z0-9\-_.\?=]+", re.IGNORECASE)


def clean_up_url(url: str, url_type: WikibaseURLType) -> str:
    """Clean URL"""

    stripped_url = url.strip()

    if url_type in [
        WikibaseURLType.BASE_URL,
        WikibaseURLType.SPARQL_ENDPOINT_URL,
        WikibaseURLType.SPARQL_FRONTEND_URL,
    ]:
        assert FULL_URL_PATTERN.match(stripped_url)
    else:
        assert not FULL_URL_PATTERN.match(stripped_url)

    return stripped_url
