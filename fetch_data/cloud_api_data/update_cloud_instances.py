"""fetch list of wikibase cloud instances from api and update local database"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data import get_async_session
from fetch_data.cloud_api_data.get_cloud_api_data import fetch_cloud_instances
from fetch_data.cloud_api_data.wikibase_cloud_instance import WikibaseCloudInstance
from logger import logger
from model.database import WikibaseModel, WikibaseURLModel
from model.enum import WikibaseType


async def _find_existing_wikibase(
    async_session: AsyncSession, cloud: WikibaseCloudInstance
) -> Optional[WikibaseModel]:
    """Finds an existing WikibaseModel based on the cloud instance domain."""
    search = f"%{cloud.domain}%"
    stmt = (
        select(WikibaseModel)
        .join(WikibaseModel.url)
        .where(WikibaseURLModel.url.like(search))
    )
    return (await async_session.scalars(stmt)).one_or_none()


def _update_existing_wikibase_if_needed(
    existing: WikibaseModel, cloud: WikibaseCloudInstance
) -> None:
    """Updates an existing WikibaseModel if changes are detected."""

    # name of a cloud instance changed
    if existing.wikibase_name != cloud.sitename:
        existing.wikibase_name = cloud.sitename
        logger.debug(
            "Updated cloud instance name to " f"{cloud.sitename} for {cloud.domain}"
        )

    # description of a cloud instance changed
    if existing.description != cloud.description:
        existing.description = cloud.description
        logger.debug(
            "Updated cloud instance description to "
            f"{cloud.description} for {cloud.domain}"
        )

    # instance moved from selfhosted to cloud
    if existing.wikibase_type != WikibaseType.CLOUD:
        existing.wikibase_type = WikibaseType.CLOUD
        existing.base_url = f"https://{cloud.domain}"
        existing.set_script_path("/w")
        existing.set_article_path("/wiki")
        existing.set_sparql_frontend_url(f"https://{cloud.domain}/query/")
        existing.set_sparql_endpoint_url(f"https://{cloud.domain}/query/sparql")
        logger.debug(f"Updated instance to be a cloud instance: {cloud.domain}")


def _create_new_wikibase(cloud: WikibaseCloudInstance) -> WikibaseModel:
    """Creates a new WikibaseModel from a cloud instance."""
    new_wikibase = WikibaseModel(
        wikibase_name=cloud.sitename,
        description=cloud.description,
        base_url=f"https://{cloud.domain}",
        script_path="/w",
        article_path="/wiki",
        sparql_frontend_url=f"https://{cloud.domain}/query/",
        sparql_endpoint_url=f"https://{cloud.domain}/query/sparql",
    )
    new_wikibase.wikibase_type = WikibaseType.CLOUD
    new_wikibase.checked = True
    logger.debug(
        f"Added new cloud instance {cloud.sitename} {cloud.domain}"
    )
    return new_wikibase


async def update_cloud_instances() -> bool:
    """
    Get the current list of known wikibase cloud instances and upsert them in the local database.
    Compares instances by domain (base URL). Updates description and sitename/wikibase_name
    if found, otherwise creates a new entry.
    """
    cloud_instances = await fetch_cloud_instances()

    async with get_async_session() as async_session:
        for cloud in cloud_instances:
            existing = await _find_existing_wikibase(async_session, cloud)

            if existing is not None:
                logger.debug(
                    "Found existing Wikibase ID "
                    + f"{existing.id} {existing.wikibase_name}"
                )
                _update_existing_wikibase_if_needed(existing, cloud)
            else:
                new_wikibase = _create_new_wikibase(cloud)
                async_session.add(new_wikibase)

        await async_session.commit()

    return True
