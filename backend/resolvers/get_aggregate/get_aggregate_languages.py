"""List of Languages"""

from typing import Optional
from sqlalchemy import Select, desc, func, not_, select
from data.database_connection import get_async_session
from model.database.wikibase_language_model import WikibaseLanguageModel
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseLanguageAggregateStrawberryModel,
)
from resolvers.util import get_filtered_wikibase_query


async def get_language_list(
    page_number: PageNumberType,
    page_size: PageSizeType,
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Page[WikibaseLanguageAggregateStrawberryModel]:
    """List of Languages"""

    wikibase_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()
    language_subquery = (
        select(WikibaseLanguageModel)
        .where(WikibaseLanguageModel.wikibase_id.in_(select(wikibase_subquery.c.id)))
        .subquery()
    )

    total_query = (
        # pylint: disable-next=not-callable
        select(language_subquery.c.language, func.count().label("total_wikibases"))
        .group_by(language_subquery.c.language)
        .subquery()
    )
    primary_query = (
        # pylint: disable-next=not-callable
        select(language_subquery.c.language, func.count().label("primary_wikibases"))
        .where(language_subquery.c.primary)
        .group_by(language_subquery.c.language)
        .subquery()
    )
    additional_query = (
        select(
            language_subquery.c.language,
            # pylint: disable-next=not-callable
            func.count().label("additional_wikibases"),
        )
        .where(not_(language_subquery.c.primary))
        .group_by(language_subquery.c.language)
        .subquery()
    )

    joined_query = (
        select(
            total_query.c.language,
            total_query.c.total_wikibases,
            primary_query.c.primary_wikibases,
            additional_query.c.additional_wikibases,
        )
        .select_from(
            total_query.join(
                primary_query,
                total_query.c.language == primary_query.c.language,
                isouter=True,
            ).join(
                additional_query,
                total_query.c.language == additional_query.c.language,
                isouter=True,
            )
        )
        .subquery()
    )
    final_query: Select[tuple[str, int, int, int]] = (
        select(
            joined_query.c.language,
            joined_query.c.total_wikibases,
            joined_query.c.primary_wikibases,
            joined_query.c.additional_wikibases,
        )
        .order_by(
            desc("primary_wikibases"),
            # desc("total_wikibases"),
            # "language",
            # joined_query.c.primary_wikibases.desc(),
            # joined_query.c.total_wikibases.desc(),
            # joined_query.c.language,
        )
        .offset((page_number - 1) * page_size)
        .limit(page_size)
    )

    async with get_async_session() as async_session:

        result = (await async_session.execute(final_query)).all()
        total_count = await async_session.scalar(
            # pylint: disable-next=not-callable
            select(func.count()).select_from(total_query)
        )

        return Page.marshal(
            page_number=page_number,
            page_size=page_size,
            total_count=total_count,
            page_data=[
                WikibaseLanguageAggregateStrawberryModel(
                    language=r[0],
                    total_wikibases=r[1],
                    primary_wikibases=r[2] or 0,
                    additional_wikibases=r[3] or 0,
                )
                for r in result
            ],
        )
