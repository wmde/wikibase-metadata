"""Clean Wikibase URL"""

import re

from urllib.parse import urlparse
from model.enum import WikibaseURLType

FULL_URL_PATTERN = re.compile(r"https?://[a-z0-9\-_.\?=/]+", re.IGNORECASE)


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    p = urlparse(url)
    host = p.hostname.lower()
    path = p.path.rstrip("/")

    return f"https://{host}{path}"


def clean_up_url(url: str, url_type: WikibaseURLType) -> str:
    """Clean URL"""

    stripped_url = url.strip()

    if url_type in [
        WikibaseURLType.BASE_URL,
        WikibaseURLType.SPARQL_ENDPOINT_URL,
        WikibaseURLType.SPARQL_FRONTEND_URL,
    ]:
        assert FULL_URL_PATTERN.match(
            stripped_url
        ), f"{url_type} must be full URL, {stripped_url}"
        
        return normalize_url(stripped_url)
    else:
        assert not FULL_URL_PATTERN.match(
            stripped_url
        ), f"{url_type} must not be full URL, {stripped_url}"

    return stripped_url
