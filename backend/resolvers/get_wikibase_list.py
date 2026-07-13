"""Get Wikibase List"""

from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from strawberry import Info
from strawberry.types.nodes import FragmentSpread, SelectedField

from data import get_async_session
from model.strawberry.input import WikibaseFilterInput, WikibaseSortInput
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseStrawberryModel,
)
from resolvers.util import get_filtered_wikibase_query, get_sorted_wikibase_query


async def get_wikibase_page(
    page_number: PageNumberType,
    page_size: PageSizeType,
    wikibase_filter: Optional[WikibaseFilterInput],
    sort_by: Optional[WikibaseSortInput],
    info: Info,
) -> Page[WikibaseStrawberryModel]:
    """Get Wikibase Page"""

    time_a = datetime.now()
    print(f"\tMethod Start {time_a}")

    query = get_filtered_wikibase_query(
        wikibase_filter, fields=compile_selected_fields(info)
    )
    query = get_sorted_wikibase_query(query, sort_by)

    time_b = datetime.now()
    print(f"\tQuery Computed {time_b}")
    print(f"\t\tDuration {time_b - time_a}")

    async with get_async_session() as async_session:
        total_count = await async_session.scalar(
            # pylint: disable-next=not-callable
            select(func.count()).select_from(query.subquery())
        )

        time_c = datetime.now()
        print(f"\tTotal Count Fetched {time_c}")
        print(f"\t\tDuration {time_c - time_a}")

        if page_size == -1:
            paginated_query = query
        else:
            paginated_query = query.offset((page_number - 1) * page_size).limit(
                page_size
            )

        time_d = datetime.now()
        print(f"\tQuery Paginated {time_d}")
        print(f"\t\tDuration {time_d - time_a}")

        results = (await async_session.scalars(paginated_query)).all()

        time_e = datetime.now()
        print(f"\tPage Data Fetched {time_e}")
        print(f"\t\tDuration {time_e - time_a}")

        result = Page.marshal(
            page_number,
            page_size,
            total_count,
            [WikibaseStrawberryModel.marshal(c) for c in results],
        )

        time_f = datetime.now()
        print(f"\tResults Marshalled {time_f}")
        print(f"\t\tDuration {time_f - time_a}")

        return result


def compile_selected_fields(info: Info) -> list[str]:
    """Get Selected Subfields Within Wikibase"""

    data_field_selections = [
        data_field_selection
        for query_selection in info.selected_fields
        if query_selection.name == "wikibaseList"
        for data_selection in query_selection.selections
        if data_selection.name == "data"
        for data_field_selection in data_selection.selections
    ]

    results = []
    for selection in data_field_selections:
        if isinstance(selection, SelectedField):
            results.append(selection.name)
        elif isinstance(selection, FragmentSpread):
            results.extend([s.name for s in selection.selections])
        else:
            raise NotImplementedError(selection)

    print(f"\tFields: {results}")
    return results
