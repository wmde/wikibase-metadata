"""fetch list of wikibase cloud instances from api and update local database"""

from data import get_async_session
from sqlalchemy import select
from model.database import WikibaseModel
from model.database.wikibase_url_model import WikibaseURLModel
from model.enum import WikibaseType

from fetch_data.utils import fetch_api_data

from logger import logger
from dataclasses import dataclass


@dataclass
class WikibaseCloudInstance:
    """cloud instance as fetched from the wikibase cloud dashboard api"""

    id: int
    description: str | None
    domain: str
    domain_decoded: str
    sitename: str | None


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
                logger.warning(f"Missing fields in cloud instance {item_dict}")

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
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)  # Join using the predefined 'url' relationship
                .where(WikibaseURLModel.url == f"https://{cloud_instance.domain}")
            )
            result = await async_session.execute(stmt)
            existing_wikibase: WikibaseModel | None = result.scalars().first()

            if existing_wikibase:
                # name of a cloud instance changed
                if existing_wikibase.wikibase_name != cloud_instance.sitename:
                    existing_wikibase.wikibase_name = cloud_instance.sitename
                    logger.debug(
                        "Updated cloud instance name to "
                        f"{cloud_instance.sitename} for {cloud_instance.domain}"
                    )

                # description of a cloud instance changed
                if existing_wikibase.description != cloud_instance.description:
                    existing_wikibase.description = cloud_instance.description
                    logger.debug(
                        "Updated cloud instance description to "
                        f"{cloud_instance.description} for {cloud_instance.domain}"
                    )

                # instance moved from selfhosted to cloud
                if existing_wikibase.wikibase_type != WikibaseType.CLOUD:
                    existing_wikibase.wikibase_type = WikibaseType.CLOUD
                    existing_wikibase.base_url = (f"https://{cloud_instance.domain}",)
                    existing_wikibase.script_path = "/w"
                    existing_wikibase.article_path = "/wiki"
                    existing_wikibase.sparql_frontend_url = (
                        f"https://{cloud_instance.domain}/query/"
                    )
                    existing_wikibase.sparql_endpoint_url = (
                        f"https://{cloud_instance.domain}/query/sparql"
                    )
                    logger.debug(
                        f"Updated instance to be a cloud instance or {cloud_instance.domain}"
                    )

            else:
                new_wikibase = WikibaseModel(
                    wikibase_name=cloud_instance.sitename,
                    description=cloud_instance.description,
                    base_url=f"https://{cloud_instance.domain}",
                    script_path="/w",
                    article_path="/wiki",
                    sparql_frontend_url=f"https://{cloud_instance.domain}/query/",
                    sparql_endpoint_url=f"https://{cloud_instance.domain}/query/sparql",
                )
                new_wikibase.wikibase_type = WikibaseType.CLOUD

                async_session.add(new_wikibase)
                logger.debug(
                    f"Added new cloud instance {cloud_instance.sitename} {cloud_instance.domain}"
                )

        await async_session.commit()
