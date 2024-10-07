"""Add Wikibase"""

from sqlalchemy import select
from data.database_connection import get_async_session
from model.database import WikibaseModel
from model.database.wikibase_category_model import WikibaseCategoryModel
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
        model = WikibaseModel(
            wikibase_name=wikibase_input.wikibase_name,
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
        category.wikibases.append(model)
        await async_session.commit()

        return model.id
