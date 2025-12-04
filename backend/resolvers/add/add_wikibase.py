"""Add Wikibase"""

from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from data.database_connection import get_async_session
from model.database import WikibaseCategoryModel, WikibaseModel, WikibaseURLModel
from model.enum import WikibaseURLType
from model.strawberry.input import WikibaseInput
from model.strawberry.output import WikibaseStrawberryModel
from resolvers.util.clean_wikibase_url import clean_up_url


async def add_wikibase(wikibase_input: WikibaseInput) -> WikibaseStrawberryModel:
    """Add Wikibase"""

    async with get_async_session() as async_session:

        assert (
            await async_session.scalar(
                # pylint: disable-next=not-callable
                select(func.count()).where(
                    WikibaseModel.wikibase_name == wikibase_input.wikibase_name.strip()
                )
            )
        ) == 0, (
            f"Wikibase with name {wikibase_input.wikibase_name.strip()} already exists"
        )

        await assert_new_url(
            async_session, wikibase_input.urls.base_url, WikibaseURLType.BASE_URL
        )
        await assert_new_url(
            async_session,
            wikibase_input.urls.sparql_endpoint_url,
            WikibaseURLType.SPARQL_ENDPOINT_URL,
        )
        await assert_new_url(
            async_session,
            wikibase_input.urls.sparql_frontend_url,
            WikibaseURLType.SPARQL_FRONTEND_URL,
        )

        model = WikibaseModel(
            wikibase_name=wikibase_input.wikibase_name.strip(),
            description=wikibase_input.description,
            organization=wikibase_input.organization,
            country=wikibase_input.country,
            region=wikibase_input.region,
            base_url=clean_up_url(
                wikibase_input.urls.base_url, WikibaseURLType.BASE_URL
            ),
            article_path=(
                clean_up_url(
                    wikibase_input.urls.article_path, WikibaseURLType.ARTICLE_PATH
                )
                if wikibase_input.urls.article_path is not None
                else None
            ),
            script_path=(
                clean_up_url(
                    wikibase_input.urls.script_path, WikibaseURLType.SCRIPT_PATH
                )
                if wikibase_input.urls.script_path is not None
                else None
            ),
            sparql_endpoint_url=(
                clean_up_url(
                    wikibase_input.urls.sparql_endpoint_url,
                    WikibaseURLType.SPARQL_ENDPOINT_URL,
                )
                if wikibase_input.urls.sparql_endpoint_url is not None
                else None
            ),
            sparql_frontend_url=(
                clean_up_url(
                    wikibase_input.urls.sparql_frontend_url,
                    WikibaseURLType.SPARQL_FRONTEND_URL,
                )
                if wikibase_input.urls.sparql_frontend_url is not None
                else None
            ),
        )
        model.checked = True
        model.category = (
            (
                await async_session.scalars(
                    select(WikibaseCategoryModel).where(
                        WikibaseCategoryModel.category == wikibase_input.category.name
                    )
                )
            ).one()
            if wikibase_input.category is not None
            else None
        )

        async_session.add(model)

        await async_session.flush()
        await async_session.refresh(model)

        returning = WikibaseStrawberryModel.marshal(model)

        await async_session.commit()

        return returning


async def assert_new_url(
    async_session: AsyncSession, input_url: Optional[str], url_type: WikibaseURLType
):
    """Assert URL Not in Database"""

    if input_url is not None:
        clean_url: str = clean_up_url(input_url, url_type)
        assert (
            await async_session.scalar(
                # pylint: disable-next=not-callable
                select(func.count()).where(WikibaseURLModel.url == clean_url)
            )
        ) == 0, f"URL {clean_url} already exists"
