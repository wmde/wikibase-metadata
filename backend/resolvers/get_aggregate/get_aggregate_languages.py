"""List of Languages"""

from typing import Optional
from sqlalchemy import case, func, select
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
    query = (
        select(
            WikibaseLanguageModel.language,
            func.count().label("total_wikibases"),
            func.sum(case((WikibaseLanguageModel.primary, 1), else_=0)).label(
                "primary_wikibases"
            ),
            func.sum(case((WikibaseLanguageModel.primary, 0), else_=1)).label(
                "additional_wikibases"
            ),
        )
        .where(WikibaseLanguageModel.wikibase_id.in_(select(wikibase_subquery.c.id)))
        .group_by(WikibaseLanguageModel.language)
    )
    paginated_query = (
        query.order_by(
            query.c.primary_wikibases.desc(),
            query.c.total_wikibases.desc(),
            query.c.language,
        )
        .offset((page_number - 1) * page_size)
        .limit(page_size)
    )

    async with get_async_session() as async_session:

        result = (await async_session.execute(paginated_query)).all()
        total_count = await async_session.scalar(
            # pylint: disable-next=not-callable
            select(func.count()).select_from(query)
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
