"""Get Wikibase List"""

from sqlalchemy import func, select

from data import get_async_session
from model.database import WikibaseModel
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseStrawberryModel,
)


async def get_wikibase_list(
    page_number: PageNumberType, page_size: PageSizeType
) -> Page[WikibaseStrawberryModel]:
    """Get Wikibase List"""

    async with get_async_session() as async_session:
        total_count = await async_session.scalar(
            select(func.count())  # pylint: disable=not-callable
            .select_from(WikibaseModel)
            .where(WikibaseModel.checked)
        )
        results = (
            await async_session.scalars(
                select(WikibaseModel)
                .where(WikibaseModel.checked)
                .order_by(WikibaseModel.id)
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
