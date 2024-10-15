"""Add Wikibase"""

from sqlalchemy import func, select
from data.database_connection import get_async_session
from model.database import WikibaseCategoryModel, WikibaseModel, WikibaseURLModel
from model.strawberry.input import WikibaseInput
from model.strawberry.output import WikibaseStrawberryModel


async def add_wikibase(wikibase_input: WikibaseInput) -> WikibaseStrawberryModel:
    """Add Wikibase"""

    async with get_async_session() as async_session:

        assert (
            await async_session.scalar(
                select(func.count()).where(  # pylint: disable=not-callable
                    WikibaseModel.wikibase_name == wikibase_input.wikibase_name.strip()
                )
            )
        ) == 0, (
            f"Wikibase with name {wikibase_input.wikibase_name.strip()} already exists"
        )

        for input_url in [
            wikibase_input.urls.action_api_url,
            wikibase_input.urls.base_url,
            wikibase_input.urls.index_api_url,
            wikibase_input.urls.sparql_endpoint_url,
            wikibase_input.urls.sparql_query_url,
            wikibase_input.urls.special_statistics_url,
            wikibase_input.urls.special_version_url,
        ]:
            if input_url is not None:
                stripped_input_url: str = input_url.strip()
                assert (
                    await async_session.scalar(
                        select(func.count()).where(  # pylint: disable=not-callable
                            WikibaseURLModel.url == stripped_input_url
                        )
                    )
                ) == 0, f"URL {stripped_input_url} already exists"

        model = WikibaseModel(
            wikibase_name=wikibase_input.wikibase_name,
            description=wikibase_input.description,
            organization=wikibase_input.organization,
            country=wikibase_input.country,
            region=wikibase_input.region,
            base_url=wikibase_input.urls.base_url,
            action_api_url=wikibase_input.urls.action_api_url,
            index_api_url=wikibase_input.urls.index_api_url,
            sparql_endpoint_url=wikibase_input.urls.sparql_endpoint_url,
            sparql_query_url=wikibase_input.urls.sparql_query_url,
            special_statistics_url=wikibase_input.urls.special_statistics_url,
            special_version_url=wikibase_input.urls.special_version_url,
        )
        model.checked = True
        model.category = (
            await async_session.scalars(
                select(WikibaseCategoryModel).where(
                    WikibaseCategoryModel.category == wikibase_input.category.name
                )
            )
        ).one()

        async_session.add(model)

        await async_session.flush()
        await async_session.refresh(model)

        returning = WikibaseStrawberryModel.marshal(model)

        await async_session.commit()

        return returning
