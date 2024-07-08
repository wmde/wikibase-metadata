"""Get Aggregate Property Popularity"""

from typing import Tuple

from sqlalchemy import Select, and_, or_, select, func

from data import get_async_session
from model.database.wikibase_observation.user.wikibase_user_group_model import (
    WikibaseUserGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_group_model import (
    WikibaseUserObservationGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_model import (
    WikibaseUserObservationModel,
)
from model.strawberry.output.observation.user.wikibase_user_aggregate import (
    WikibaseUserAggregate,
)


async def get_aggregate_users() -> WikibaseUserAggregate:
    """Get Aggregate Property Popularity"""

    total_user_query = get_total_user_query()
    total_admin_query = get_total_admin_query()

    async with get_async_session() as async_session:
        total_users, wikibase_count = (
            await async_session.execute(total_user_query)
        ).one()
        (total_admin,) = (await async_session.execute(total_admin_query)).one()

        return WikibaseUserAggregate(
            total_admin=total_admin,
            total_users=total_users,
            wikibase_count=wikibase_count,
        )


def get_total_admin_query() -> Select[Tuple[int]]:
    """Get Total Admin Query"""

    rank_subquery = (
        select(
            WikibaseUserObservationModel.id,
            func.rank()  # pylint: disable=not-callable
            .over(
                partition_by=WikibaseUserObservationModel.wikibase_id,
                order_by=WikibaseUserObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(WikibaseUserObservationModel.returned_data)
        .subquery()
    )
    query = (
        select(
            func.sum(WikibaseUserObservationGroupModel.user_count).label("total_admins")
        )
        .join(
            rank_subquery,
            onclause=WikibaseUserObservationGroupModel.wikibase_user_observation_id
            == rank_subquery.c.id,
        )
        .where(
            and_(
                rank_subquery.c.rank == 1,
                WikibaseUserObservationGroupModel.user_group.has(
                    or_(
                        WikibaseUserGroupModel.group_name.in_(["bureaucrat", "sysop"]),
                        WikibaseUserGroupModel.group_name.like(r"%admin%"),
                    )
                ),
            )
        )
    )
    return query


def get_total_user_query() -> Select[Tuple[int, int]]:
    """Get Total User Query"""

    rank_subquery = (
        select(
            WikibaseUserObservationModel,
            func.rank()  # pylint: disable=not-callable
            .over(
                partition_by=WikibaseUserObservationModel.wikibase_id,
                order_by=WikibaseUserObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(WikibaseUserObservationModel.returned_data)
        .subquery()
    )
    query = (
        select(
            func.sum(WikibaseUserObservationModel.total_users).label("total_users"),
            func.count().label("wikibase_count"),  # pylint: disable=not-callable
        )
        .join(
            rank_subquery,
            onclause=WikibaseUserObservationModel.id == rank_subquery.c.id,
        )
        .where(rank_subquery.c.rank == 1)
    )
    return query
