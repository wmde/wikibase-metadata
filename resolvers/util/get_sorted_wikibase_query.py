"""Get Filtered Wikibase Query"""

from typing import Optional

from sqlalchemy import Select, and_, func, select

from model.database import (
    WikibaseModel,
    WikibaseQuantityObservationModel,
    WikibaseRecentChangesObservationModel,
)
from model.strawberry.input import SortColumnEnum, SortDirEnum, WikibaseSortInput

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
RC_RANK = (
    select(
        WikibaseRecentChangesObservationModel.id,
        WikibaseRecentChangesObservationModel.wikibase_id,
        # pylint: disable-next=not-callable
        func.rank()
        .over(
            partition_by=WikibaseRecentChangesObservationModel.wikibase_id,
            order_by=[
                WikibaseRecentChangesObservationModel.observation_date.desc(),
                WikibaseRecentChangesObservationModel.id,
            ],
        )
        .label("rank"),
    )
    .where((WikibaseRecentChangesObservationModel.returned_data))
    .cte("recent_changes_rank_subquery")
)


def get_sorted_wikibase_query(
    query: Select[tuple[WikibaseModel]], sort_by: Optional[WikibaseSortInput] = None
) -> Select[tuple[WikibaseModel]]:
    """Sorted list of Wikibases"""

    if sort_by is None:
        return query

    match sort_by.column:
        case SortColumnEnum.CATEGORY:
            query = query.order_by(
                WikibaseModel.category_id.asc()
                if sort_by.dir == SortDirEnum.ASC
                else WikibaseModel.category_id.desc()
            )

        case SortColumnEnum.EDITS:
            query = (
                query.join(
                    RC_RANK,
                    isouter=True,
                    onclause=and_(
                        WikibaseModel.id == RC_RANK.c.wikibase_id,
                        RC_RANK.c.rank == 1,
                    ),
                )
                .join(
                    WikibaseRecentChangesObservationModel,
                    isouter=True,
                    onclause=RC_RANK.c.id == WikibaseRecentChangesObservationModel.id,
                )
                .order_by(
                    (
                        WikibaseRecentChangesObservationModel.bot_change_count
                        + WikibaseRecentChangesObservationModel.human_change_count
                    ).asc()
                    if sort_by.dir == SortDirEnum.ASC
                    else (
                        WikibaseRecentChangesObservationModel.bot_change_count
                        + WikibaseRecentChangesObservationModel.human_change_count
                    ).desc()
                )
            )

        case SortColumnEnum.TITLE:
            query = query.order_by(
                WikibaseModel.wikibase_name.asc()
                if sort_by.dir == SortDirEnum.ASC
                else WikibaseModel.wikibase_name.desc()
            )

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

        case SortColumnEnum.TYPE:
            query = query.order_by(
                WikibaseModel.wikibase_type.asc()
                if sort_by.dir == SortDirEnum.ASC
                else WikibaseModel.wikibase_type.desc()
            )

    return query
