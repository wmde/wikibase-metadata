"""List of Languages"""

from sqlalchemy import Select, func, not_, select
from data.database_connection import get_async_session
from model.database.wikibase_language_model import WikibaseLanguageModel
from model.strawberry.output import (
    AggregateLanguageStrawberryModel,
    Page,
    PageNumberType,
    PageSizeType,
)


async def get_language_list(
    page_number: PageNumberType,
    page_size: PageSizeType,
) -> Page[AggregateLanguageStrawberryModel]:
    """List of Languages"""

    total_query = (
        # pylint: disable-next=not-callable
        select(WikibaseLanguageModel.language, func.count().label("total_wikibases"))
        .group_by(WikibaseLanguageModel.language)
        .subquery()
    )
    primary_query = (
        # pylint: disable-next=not-callable
        select(WikibaseLanguageModel.language, func.count().label("primary_wikibases"))
        .where(WikibaseLanguageModel.primary)
        .group_by(WikibaseLanguageModel.language)
        .subquery()
    )
    additional_query = (
        select(
            WikibaseLanguageModel.language,
            # pylint: disable-next=not-callable
            func.count().label("additional_wikibases"),
        )
        .where(not_(WikibaseLanguageModel.primary))
        .group_by(WikibaseLanguageModel.language)
        .subquery()
    )

    final_query: Select[tuple[str, int, int, int]] = (
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
        .order_by(total_query.c.total_wikibases.desc())
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
                AggregateLanguageStrawberryModel(
                    language=r[0],
                    total_wikibases=r[1],
                    primary_wikibases=r[2] or 0,
                    additional_wikibases=r[3] or 0,
                )
                for r in result
            ],
        )
