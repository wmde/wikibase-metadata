"""Fix"""

from requests.exceptions import HTTPError
from sqlalchemy import and_, or_, select

from data import get_async_session
from fetch_data.utils.fetch_data_from_api import fetch_api_data
from logger import logger
from model.database import (
    WikibaseModel,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseSoftwareModel,
    WikibaseURLModel,
)
from model.enum import WikibaseURLType
from resolvers.update.update_wikibase_url import upsert_wikibase_url


async def update_missing_sparql_urls():
    """Attempt to Fetch SPARQL Paths from Manifest"""

    script_path_subquery = (
        select(WikibaseURLModel)
        .where(WikibaseURLModel.url_type == WikibaseURLType.SCRIPT_PATH)
        .subquery()
    )
    sparql_endpoint_subquery = (
        select(WikibaseURLModel)
        .where(WikibaseURLModel.url_type == WikibaseURLType.SPARQL_ENDPOINT_URL)
        .subquery()
    )
    sparql_frontend_subquery = (
        select(WikibaseURLModel)
        .where(WikibaseURLModel.url_type == WikibaseURLType.SPARQL_FRONTEND_URL)
        .subquery()
    )
    query = (
        select(WikibaseModel)
        .where(WikibaseModel.checked)
        .join(
            script_path_subquery,
            onclause=WikibaseModel.id == script_path_subquery.c.wikibase_id,
            isouter=False,
        )
        .join(
            sparql_endpoint_subquery,
            onclause=WikibaseModel.id == sparql_endpoint_subquery.c.wikibase_id,
            isouter=True,
        )
        .join(
            sparql_frontend_subquery,
            onclause=WikibaseModel.id == sparql_frontend_subquery.c.wikibase_id,
            isouter=True,
        )
        .where(
            and_(
                WikibaseModel.software_version_observations.any(
                    WikibaseSoftwareVersionObservationModel.software_versions.any(
                        WikibaseSoftwareVersionModel.software.has(
                            WikibaseSoftwareModel.software_name == "WikibaseManifest"
                        )
                    )
                ),
                or_(
                    # pylint: disable-next=singleton-comparison
                    sparql_endpoint_subquery.c.id == None,
                    # pylint: disable-next=singleton-comparison
                    sparql_frontend_subquery.c.id == None,
                ),
            )
        )
    )

    async with get_async_session() as async_session:
        wikis = (await async_session.scalars(query)).all()

        logger.info(f"Missing SPARQL Path: {len(wikis)}")

        for wikibase in wikis:
            await fetch_wikibase_sparql_urls(wikibase)
        return len(wikis)


async def fetch_wikibase_sparql_urls(wikibase: WikibaseModel):
    """Attempt to Fetch SPARQL Paths from Manifest"""

    assert wikibase.rest_api_url() is not None

    try:
        manifest_data = await fetch_api_data(
            wikibase.rest_api_url() + "/wikibase-manifest/v0/manifest"
        )
        if "external_services" in manifest_data:
            if wikibase.sparql_endpoint_url is None:
                assert await upsert_wikibase_url(
                    wikibase.id,
                    manifest_data["external_services"].get("queryservice"),
                    WikibaseURLType.SPARQL_ENDPOINT_URL,
                )
            if wikibase.sparql_frontend_url is None:
                assert await upsert_wikibase_url(
                    wikibase.id,
                    manifest_data["external_services"].get("queryservice_ui"),
                    WikibaseURLType.SPARQL_FRONTEND_URL,
                )

    except HTTPError:
        pass
