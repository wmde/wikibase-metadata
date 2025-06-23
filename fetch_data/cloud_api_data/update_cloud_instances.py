"""fetch list of wikibase cloud instances from api and update local database"""

from logger import logger
from typing import Optional

from data import get_async_session
from sqlalchemy import select
from model.database import WikibaseModel
from model.database.wikibase_url_model import WikibaseURLModel
from model.enum import WikibaseType

from fetch_data.cloud_api_data import fetch_cloud_instances


async def update_cloud_instances() -> bool:
    """
    Get the current list of known wikibase cloud instances and upsert them in the local database.
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
            existing_wikibase: Optional[WikibaseModel] = (
                await async_session.scalars(stmt)
            ).one_or_none()

            if existing_wikibase is not None:
                logger.debug(
                    "Found existing Wikibase ID "
                    + f"{existing_wikibase.id} {existing_wikibase.wikibase_name}"
                )

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
                    existing_wikibase.set_script_path("/w")
                    existing_wikibase.set_article_path("/wiki")
                    existing_wikibase.set_sparql_frontend_url(
                        f"https://{cloud_instance.domain}/query/"
                    )
                    existing_wikibase.set_sparql_endpoint_url(
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
                # TODO: what is this checked for? is it reasonable to set it to checked here?
                new_wikibase.checked = True

                async_session.add(new_wikibase)
                logger.debug(
                    f"Added new cloud instance {cloud_instance.sitename} {cloud_instance.domain}"
                )

        await async_session.commit()
        return True
