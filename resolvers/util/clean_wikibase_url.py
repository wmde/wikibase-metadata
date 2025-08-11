"""Clean Wikibase URL"""

import re

from model.enum import WikibaseURLType


def clean_up_url(url: str, url_type: WikibaseURLType) -> str:
    """Clean URL"""

    if url_type in [
        WikibaseURLType.BASE_URL,
        WikibaseURLType.SPARQL_ENDPOINT_URL,
        WikibaseURLType.SPARQL_FRONTEND_URL,
    ]:
        assert re.match(r"https?://[A-z0-9\-_.\?=]+", url)

    return url.strip()
