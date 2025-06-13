from data import get_async_session
from sqlalchemy import select
from model.database import WikibaseModel
from model.database.wikibase_url_model import WikibaseURLModel
from model.enum import WikibaseType

from fetch_data.utils import fetch_api_data

from logger import logger


class WikibaseCloudInstance:
    id: int
    description: str | None
    domain: str
    domain_decoded: str
    sitename: str | None

    def __init__(
        self,
        id: int,
        description: str | None,
        domain: str,
        domain_decoded: str,
        sitename: str | None,
    ):
        self.id = id
        self.description = description
        self.domain = domain
        self.domain_decoded = domain_decoded
        self.sitename = sitename


async def fetch_cloud_instances() -> list[WikibaseCloudInstance]:
    """
    Get the list of currently known wikibase cloud instances
    from the wikibase cloud dashboard api
    """
    url = "https://www.wikibase.cloud/api/wiki?page=1&per_page=10000"
    query_data = await fetch_api_data(url)

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
                logger.warn(f"Missing fields in cloud instance {item_dict}")

    return instances


async def update_cloud_instances():
    """
    Get the current list of known wikibase cloud instances and
    upsert them in the local database.
    Compares instances by domain (base URL). Updates description and sitename/wikibase_name
    if found, otherwise creates a new entry.
    """
    cloud_instances = await fetch_cloud_instances()

    async with get_async_session() as async_session:
        for cloud_instance in cloud_instances:
            # Query for an existing WikibaseModel based on its base URL
            # The WikibaseModel.url relationship points to the WikibaseURLModel for the BASE_URL
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)  # Join using the predefined 'url' relationship
                .where(WikibaseURLModel.url == cloud_instance.domain)
            )
            result = await async_session.execute(stmt)
            # logger.debug(f"{len(result)}")
            existing_wikibase: WikibaseModel | None = result.scalars().first()
            # logger.debug(existing_wikibase)
            # logger.debug(existing_wikibase.url.url)

            if existing_wikibase:
                # Update existing entry
                existing_wikibase.wikibase_name = cloud_instance.sitename
                existing_wikibase.description = cloud_instance.description
                logger.debug("updated")
            else:
                # Create new entry
                new_wikibase = WikibaseModel(
                    wikibase_name=cloud_instance.sitename,
                    base_url=cloud_instance.domain,
                    description=cloud_instance.description,
                    # Other fields like article_path, script_path will be None by default
                    # as per WikibaseModel.__init__
                )
                new_wikibase.wikibase_type = WikibaseType.CLOUD
                async_session.add(new_wikibase)
                logger.debug("inserted")

        await async_session.commit()

