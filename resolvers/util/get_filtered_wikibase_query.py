"""Get Filtered Wikibase Query"""

from typing import Optional

from sqlalchemy import Select, select

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
                WikibaseModel.wikibase_type.not_in(
                    wikibase_filter.wikibase_type.exclude
                )
            )
        # if filter.wikibase_type.include is not None:
        #     query = query.where(WikibaseModel.wikibase_type.in_(filter.wikibase_type.include))
    return query
