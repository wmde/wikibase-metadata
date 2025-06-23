"""fetch list of wikibase cloud instances from api and update local database"""

from dataclasses import dataclass
from logger import logger

from fetch_data.utils import fetch_api_data


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


URL = "https://www.wikibase.cloud/api/wiki?page=1&per_page=10000"

async def fetch_cloud_instances() -> list[WikibaseCloudInstance]:
    """
    Get the list of currently known wikibase cloud instances
    from the wikibase cloud dashboard api
    """
    query_data = await fetch_api_data(URL)

    instances: list[WikibaseCloudInstance] = []
    if query_data and "data" in query_data:
        for item_dict in query_data["data"]:
            logger.debug(f"fetched cloud instance {item_dict}")

            raw_id = item_dict.get("id")
            raw_description = item_dict.get("description")
            raw_domain = item_dict.get("domain")
            raw_domain_decoded = item_dict.get("domain_decoded")
            raw_sitename = item_dict.get("sitename")

            if (
                raw_id is not None
                and raw_domain is not None
                and raw_domain_decoded is not None
            ):
                instance = WikibaseCloudInstance(
                    id=raw_id,
                    description=raw_description,
                    domain=raw_domain,
                    domain_decoded=raw_domain_decoded,
                    sitename=raw_sitename,
                )
                instances.append(instance)
            else:
                logger.warning(f"Missing fields in cloud instance {item_dict}")

    return instances
