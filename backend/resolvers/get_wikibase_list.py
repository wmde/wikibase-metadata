"""Get Wikibase List"""

from typing import Any, Optional
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from model.database import WikibaseModel
from model.strawberry.input import WikibaseFilterInput, WikibaseSortInput
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseStrawberryModel,
)
from resolvers.util import get_filtered_wikibase_query, get_sorted_wikibase_query


async def get_wikibase_page(
    async_session: Any,
    page_number: PageNumberType,
    page_size: PageSizeType,
    wikibase_filter: Optional[WikibaseFilterInput],
    sort_by: Optional[WikibaseSortInput],
) -> Page[WikibaseStrawberryModel]:
    """Get Wikibase Page"""

    query = get_filtered_wikibase_query(wikibase_filter)
    query = get_sorted_wikibase_query(query, sort_by)

    total_count = await async_session.scalar(
        # pylint: disable-next=not-callable
        select(func.count()).select_from(query.subquery())
    )
    base_query = (
    query.order_by(WikibaseModel.id)
    .options(
        selectinload(WikibaseModel.primary_language),
        selectinload(WikibaseModel.additional_languages),
        selectinload(WikibaseModel.url),
        selectinload(WikibaseModel.article_path),
        selectinload(WikibaseModel.script_path),
        selectinload(WikibaseModel.sparql_endpoint_url),
        selectinload(WikibaseModel.sparql_frontend_url),
        selectinload(WikibaseModel.category),
        selectinload(WikibaseModel.connectivity_observations),
        selectinload(WikibaseModel.external_identifier_observations),
        selectinload(WikibaseModel.log_month_observations),
        selectinload(WikibaseModel.property_popularity_observations),
        selectinload(WikibaseModel.quantity_observations),
        selectinload(WikibaseModel.recent_changes_observations),
        selectinload(WikibaseModel.software_version_observations),
        selectinload(WikibaseModel.statistics_observations),
        selectinload(WikibaseModel.time_to_first_value_observations),
        selectinload(WikibaseModel.user_observations),
        )
    )

    if page_size == -1:
        paginated_query = base_query
    else:
        paginated_query = (
            base_query
            .offset((page_number - 1) * page_size)
            .limit(page_size)
        )

    results = (await async_session.scalars(paginated_query)).all()

    return Page.marshal(
        page_number,
        page_size,
        total_count,
        [WikibaseStrawberryModel.marshal(c) for c in results],
    )