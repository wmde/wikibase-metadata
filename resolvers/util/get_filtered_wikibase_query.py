"""Get Filtered Wikibase Query"""

from typing import Optional

from sqlalchemy import Select, or_, select

from model.database import WikibaseModel
from model.enum import WikibaseType
from model.strawberry.input import WikibaseFilterInput


def get_filtered_wikibase_query(
    wikibase_filter: Optional[WikibaseFilterInput] = None,
) -> Select[tuple[WikibaseModel]]:
    """Filtered list of Wikibases"""

    query = select(WikibaseModel).where(WikibaseModel.checked)
    if wikibase_filter is None:
        return query

    if wikibase_filter.wikibase_type is not None:
        if (
            wikibase_filter.wikibase_type.exclude is not None
            and len(wikibase_filter.wikibase_type.exclude) > 0
        ):
            if WikibaseType.UNKNOWN in wikibase_filter.wikibase_type.exclude:
                query = query.where(
                    WikibaseModel.wikibase_type.notin_(
                        wikibase_filter.wikibase_type.exclude
                    )
                )
            else:
                query = query.where(
                    or_(
                        # pylint: disable-next=singleton-comparison
                        WikibaseModel.wikibase_type == None,
                        WikibaseModel.wikibase_type.notin_(
                            wikibase_filter.wikibase_type.exclude
                        ),
                    )
                )

        if (
            wikibase_filter.wikibase_type.include is not None
            and len(wikibase_filter.wikibase_type.include) > 0
        ):
            if WikibaseType.UNKNOWN in wikibase_filter.wikibase_type.include:
                query = query.where(
                    or_(
                        # pylint: disable-next=singleton-comparison
                        WikibaseModel.wikibase_type == None,
                        WikibaseModel.wikibase_type.in_(
                            wikibase_filter.wikibase_type.include
                        ),
                    )
                )
            else:
                query = query.where(
                    WikibaseModel.wikibase_type.in_(
                        wikibase_filter.wikibase_type.include
                    )
                )

    return query
