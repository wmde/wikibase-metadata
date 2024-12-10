"""Get Wikibase List"""

from sqlalchemy import func, select

from data import get_async_session
from model.database import WikibaseSoftwareModel
from model.enum import WikibaseSoftwareType
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseSoftwareStrawberryModel,
)


async def get_software_list(
    page_number: PageNumberType,
    page_size: PageSizeType,
    software_type: WikibaseSoftwareType,
) -> Page[WikibaseSoftwareStrawberryModel]:
    """Get Wikibase List"""

    async with get_async_session() as async_session:
        total_count = await async_session.scalar(
            # pylint: disable-next=not-callable
            select(func.count())
            .select_from(WikibaseSoftwareModel)
            .where(WikibaseSoftwareModel.software_type == software_type)
        )
        results = (
            await async_session.scalars(
                select(WikibaseSoftwareModel)
                .where(WikibaseSoftwareModel.software_type == software_type)
                .order_by(
                    WikibaseSoftwareModel.software_type,
                    WikibaseSoftwareModel.software_name,
                )
                .offset((page_number - 1) * page_size)
                .limit(page_size)
            )
        ).all()
        return Page.marshal(
            page_number,
            page_size,
            total_count,
            [WikibaseSoftwareStrawberryModel.marshal(c) for c in results],
        )
