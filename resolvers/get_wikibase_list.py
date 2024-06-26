"""Get Wikibase List"""

from sqlalchemy import func, select

from data.database_connection import get_async_session
from model.database import WikibaseModel
from model.strawberry.output import WikibaseStrawberryModel
from model.strawberry.output.page import Page


async def get_wikibase_list(
    page_number: int, page_size: int
) -> Page[WikibaseStrawberryModel]:
    """Get Wikibase List"""

    async with get_async_session() as async_session:
        total_count = await async_session.scalar(
            select(func.count()).select_from(  # pylint: disable=not-callable
                WikibaseModel
            )
        )
        results = (
            await async_session.scalars(
                select(WikibaseModel)
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
