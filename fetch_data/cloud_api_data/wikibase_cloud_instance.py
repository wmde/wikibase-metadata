from dataclasses import dataclass


@dataclass
class WikibaseCloudInstance:
    """cloud instance as fetched from the wikibase cloud dashboard api"""

    id: int
    description: str | None

    # domain is PUNYcode, domain_decoded is unicode.
    #  e.g.
    #   "domain":"xn--brgerspitalzinshaus-59b.wikibase.cloud"
    #   "domain_decoded":"b\u00fcrgerspitalzinshaus.wikibase.cloud"
    domain: str
    domain_decoded: str

    sitename: str | None
