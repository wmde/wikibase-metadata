"""Add Wikibase"""

from sqlalchemy import func, select
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

        for input_url in [
            wikibase_input.urls.base_url,
            wikibase_input.urls.sparql_endpoint_url,
            wikibase_input.urls.sparql_frontend_url,
        ]:
            if input_url is not None:
                clean_url: str = clean_up_url(input_url, WikibaseURLType.BASE_URL)
                assert (
                    await async_session.scalar(
                        # pylint: disable-next=not-callable
                        select(func.count()).where(WikibaseURLModel.url == clean_url)
                    )
                ) == 0, f"URL {clean_url} already exists"

        model = WikibaseModel(
            wikibase_name=wikibase_input.wikibase_name,
            description=wikibase_input.description,
            organization=wikibase_input.organization,
            country=wikibase_input.country,
            region=wikibase_input.region,
            base_url=wikibase_input.urls.base_url,
            article_path=wikibase_input.urls.article_path,
            script_path=wikibase_input.urls.script_path,
            sparql_endpoint_url=wikibase_input.urls.sparql_endpoint_url,
            sparql_frontend_url=wikibase_input.urls.sparql_frontend_url,
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
