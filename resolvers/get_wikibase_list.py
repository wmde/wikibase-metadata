"""Get Wikibase List"""

from typing import Optional
from sqlalchemy import func, select

from data import get_async_session
from model.database import WikibaseModel
from model.strawberry.input import WikibaseFilterInput, WikibaseSortInput
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseStrawberryModel,
)
from resolvers.util import get_filtered_wikibase_query


async def get_wikibase_page(
    page_number: PageNumberType,
    page_size: PageSizeType,
    wikibase_filter: Optional[WikibaseFilterInput],
    sort_by: Optional[WikibaseSortInput],
) -> Page[WikibaseStrawberryModel]:
    """Get Wikibase Page"""

    query = get_filtered_wikibase_query(wikibase_filter, sort_by)

    async with get_async_session() as async_session:
        total_count = await async_session.scalar(
            # pylint: disable-next=not-callable
            select(func.count()).select_from(query.subquery())
        )
        results = (
            await async_session.scalars(
                query.order_by(WikibaseModel.id)
                .offset((page_number - 1) * page_size)
                .limit(page_size)
            )
        ).all()
        return Page.marshal(
            page_number,
            page_size,
            total_count,
            [WikibaseStrawberryModel.marshal(c) for c in results],
        )
