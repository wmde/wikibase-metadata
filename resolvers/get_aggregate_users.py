"""Get Aggregate Users"""

from typing import Optional
from sqlalchemy import Select, and_, or_, select, func

from data import get_async_session
from model.database import (
    WikibaseUserGroupModel,
    WikibaseUserObservationGroupModel,
    WikibaseUserObservationModel,
)
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import WikibaseUserAggregateStrawberryModel
from resolvers.util import get_filtered_wikibase_query


async def get_aggregate_users(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> WikibaseUserAggregateStrawberryModel:
    """Get Aggregate Users"""

    total_user_query = get_total_user_query(wikibase_filter)
    total_admin_query = get_total_admin_query(wikibase_filter)

    async with get_async_session() as async_session:
        total_users, users_wikibase_count = (
            await async_session.execute(total_user_query)
        ).one()
        total_admin, admin_wikibase_count = (
            await async_session.execute(total_admin_query)
        ).one()
        assert users_wikibase_count == admin_wikibase_count

        return WikibaseUserAggregateStrawberryModel(
            total_admin=total_admin or 0,
            total_users=total_users or 0,
            wikibase_count=users_wikibase_count,
        )


def get_total_admin_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, int]]:
    """Get Total Admin Query"""

    filtered_wikibase_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()

    rank_subquery = (
        select(
            WikibaseUserObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseUserObservationModel.wikibase_id,
                order_by=WikibaseUserObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_wikibase_subquery,
            onclause=WikibaseUserObservationModel.wikibase_id
            == filtered_wikibase_subquery.c.id,
        )
        .where(WikibaseUserObservationModel.returned_data)
        .subquery()
    )

    group_subquery = (
        select(func.max(WikibaseUserObservationGroupModel.user_count).label("admins"))
        .join(
            rank_subquery,
            onclause=and_(
                WikibaseUserObservationGroupModel.wikibase_user_observation_id
                == rank_subquery.c.id,
                rank_subquery.c.rank == 1,
            ),
        )
        .where(
            WikibaseUserObservationGroupModel.user_group.has(
                or_(
                    WikibaseUserGroupModel.group_name.in_(["bureaucrat", "sysop"]),
                    WikibaseUserGroupModel.group_name.like(r"%admin%"),
                )
            )
        )
        .group_by(WikibaseUserObservationGroupModel.wikibase_user_observation_id)
        .subquery()
    )

    query = select(
        func.sum(group_subquery.c.admins).label("total_admins"),
        # pylint: disable-next=not-callable
        func.count().label("wikibase_count"),
    )

    return query


def get_total_user_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, int]]:
    """Get Total User Query"""

    filtered_wikibase_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()

    rank_subquery = (
        select(
            WikibaseUserObservationModel,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseUserObservationModel.wikibase_id,
                order_by=WikibaseUserObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_wikibase_subquery,
            onclause=WikibaseUserObservationModel.wikibase_id
            == filtered_wikibase_subquery.c.id,
        )
        .where(
            WikibaseUserObservationModel.returned_data,
        )
        .subquery()
    )
    query = select(
        func.sum(WikibaseUserObservationModel.total_users).label("total_users"),
        # pylint: disable-next=not-callable
        func.count().label("wikibase_count"),
    ).join(
        rank_subquery,
        onclause=and_(
            WikibaseUserObservationModel.id == rank_subquery.c.id,
            rank_subquery.c.rank == 1,
        ),
    )

    return query
