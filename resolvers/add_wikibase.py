"""Add Wikibase"""

from sqlalchemy import func, select
from data.database_connection import get_async_session
from model.database import WikibaseCategoryModel, WikibaseModel, WikibaseURLModel
from model.strawberry.input import WikibaseInput


async def add_wikibase(wikibase_input: WikibaseInput) -> int:
    """Add Wikibase"""

    async with get_async_session() as async_session:

        category = (
            await async_session.scalars(
                select(WikibaseCategoryModel).where(
                    WikibaseCategoryModel.category == wikibase_input.category.name
                )
            )
        ).one()

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
                assert (
                    await async_session.scalar(
                        select(func.count()).where(  # pylint: disable=not-callable
                            WikibaseURLModel.url == input_url.strip()
                        )
                    )
                ) == 0, f"URL {input_url.strip()} already exists"

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
            sparql_query_url=wikibase_input.urls.sparql_endpoint_url,
            special_statistics_url=wikibase_input.urls.special_statistics_url,
            special_version_url=wikibase_input.urls.special_version_url,
        )
        model.checked = True
        category.wikibases.append(model)
        await async_session.commit()

        return model.id
