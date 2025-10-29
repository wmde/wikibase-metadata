"""Get Filtered Wikibase Query"""

from typing import Optional

from sqlalchemy import Select, and_, func, or_, select

from model.database import (
    WikibaseModel,
)
from model.database import WikibaseQuantityObservationModel
from model.strawberry.input import (
    SortColumnEnum,
    SortDirEnum,
    WikibaseFilterInput,
    WikibaseSortInput,
)

Q_RANK = (
    select(
        WikibaseQuantityObservationModel.id,
        WikibaseQuantityObservationModel.wikibase_id,
        # pylint: disable-next=not-callable
        func.rank()
        .over(
            partition_by=WikibaseQuantityObservationModel.wikibase_id,
            order_by=[
                WikibaseQuantityObservationModel.observation_date.desc(),
                WikibaseQuantityObservationModel.id,
            ],
        )
        .label("rank"),
    )
    .where((WikibaseQuantityObservationModel.returned_data))
    .cte("quantity_rank_subquery")
)


def get_filtered_wikibase_query(
    wikibase_filter: Optional[WikibaseFilterInput] = None,
    sort_by: Optional[WikibaseSortInput] = None,
) -> Select[tuple[WikibaseModel]]:
    """Filtered list of Wikibases"""

    query = select(WikibaseModel).where(WikibaseModel.checked)
    if wikibase_filter is None and sort_by is None:
        return query

    if wikibase_filter is not None:
        if wikibase_filter.wikibase_type is not None:
            if (
                wikibase_filter.wikibase_type.exclude is not None
                and len(wikibase_filter.wikibase_type.exclude) > 0
            ):
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
                query = query.where(
                    WikibaseModel.wikibase_type.in_(
                        wikibase_filter.wikibase_type.include
                    )
                )

    if sort_by is not None:
        match sort_by.column:
            case SortColumnEnum.TRIPLES:
                query = (
                    query.join(
                        Q_RANK,
                        isouter=True,
                        onclause=and_(
                            WikibaseModel.id == Q_RANK.c.wikibase_id, Q_RANK.c.rank == 1
                        ),
                    )
                    .join(
                        WikibaseQuantityObservationModel,
                        isouter=True,
                        onclause=Q_RANK.c.id == WikibaseQuantityObservationModel.id,
                    )
                    .order_by(
                        WikibaseQuantityObservationModel.total_triples.asc()
                        if sort_by.dir == SortDirEnum.ASC
                        else WikibaseQuantityObservationModel.total_triples.desc()
                    )
                )

    return query
