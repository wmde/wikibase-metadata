"""Get Filtered Wikibase Query"""

from typing import Optional

from sqlalchemy import Select, or_, select

from model.database import (
    WikibaseModel,
)
from model.strawberry.input import WikibaseFilterInput


def get_filtered_wikibase_query(
    wikibase_filter: Optional[WikibaseFilterInput] = None,
) -> Select[tuple[WikibaseModel]]:
    """Filtered list of Wikibases"""

    query = select(WikibaseModel).where(WikibaseModel.checked)
    if wikibase_filter is None:
        return query

    if wikibase_filter.wikibase_type is not None:
        if wikibase_filter.wikibase_type.exclude is not None:
            query = query.where(
                or_(
                    # pylint: disable-next=singleton-comparison
                    WikibaseModel.wikibase_type == None,
                    WikibaseModel.wikibase_type.notin_(
                        wikibase_filter.wikibase_type.exclude
                    ),
                )
            )
    return query
