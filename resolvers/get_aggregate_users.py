"""Get Aggregate Users"""

from sqlalchemy import Select, and_, or_, select, func

from data import get_async_session
from model.database import (
    WikibaseModel,
    WikibaseUserGroupModel,
    WikibaseUserObservationGroupModel,
    WikibaseUserObservationModel,
)
from model.strawberry.output import WikibaseUserAggregateStrawberryModel


async def get_aggregate_users() -> WikibaseUserAggregateStrawberryModel:
    """Get Aggregate Users"""

    total_user_query = get_total_user_query()
    total_admin_query = get_total_admin_query()

    async with get_async_session() as async_session:
        total_users, users_wikibase_count = (
            await async_session.execute(total_user_query)
        ).one()
        total_admin, admin_wikibase_count = (
            await async_session.execute(total_admin_query)
        ).one()
        assert users_wikibase_count == admin_wikibase_count

        return WikibaseUserAggregateStrawberryModel(
            total_admin=total_admin,
            total_users=total_users,
            wikibase_count=users_wikibase_count,
        )


def get_total_admin_query() -> Select[tuple[int, int]]:
    """Get Total Admin Query"""

    rank_subquery = (
        select(
            WikibaseUserObservationModel.id,
            # pylint: disable=not-callable
            func.rank()
            .over(
                partition_by=WikibaseUserObservationModel.wikibase_id,
                order_by=WikibaseUserObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(
            and_(
                WikibaseUserObservationModel.returned_data,
                WikibaseUserObservationModel.wikibase.has(WikibaseModel.checked),
            )
        )
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
        # pylint: disable=not-callable
        func.count().label("wikibase_count"),
    )

    return query


def get_total_user_query() -> Select[tuple[int, int]]:
    """Get Total User Query"""

    rank_subquery = (
        select(
            WikibaseUserObservationModel,
            # pylint: disable=not-callable
            func.rank()
            .over(
                partition_by=WikibaseUserObservationModel.wikibase_id,
                order_by=WikibaseUserObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(
            and_(
                WikibaseUserObservationModel.returned_data,
                WikibaseUserObservationModel.wikibase.has(WikibaseModel.checked),
            )
        )
        .subquery()
    )
    query = select(
        func.sum(WikibaseUserObservationModel.total_users).label("total_users"),
        # pylint: disable=not-callable
        func.count().label("wikibase_count"),
    ).join(
        rank_subquery,
        onclause=and_(
            WikibaseUserObservationModel.id == rank_subquery.c.id,
            rank_subquery.c.rank == 1,
        ),
    )

    return query
