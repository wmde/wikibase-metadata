"""Get Out of Date Wikibases"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import Select, and_, not_, or_, select
from data.database_connection import get_async_session
from model.database import (
    WikibaseConnectivityObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseStatisticsObservationModel,
    WikibaseUserObservationModel,
)


async def get_wikibase_list(query: Select[tuple[WikibaseModel]]) -> list[WikibaseModel]:
    """Get List of Wikibases from Query"""

    async with get_async_session() as async_session:
        wikibase_list = (await async_session.scalars(query)).unique().all()
        return wikibase_list


def get_wikibase_with_out_of_date_connectivity_obs_query() -> (
    Select[tuple[WikibaseModel]]
):
    """Query Wikibases with Out of Date Connectivity Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            not_(
                WikibaseModel.connectivity_observations.any(
                    or_(
                        WikibaseConnectivityObservationModel.observation_date
                        > (datetime.now(tz=timezone.utc) - timedelta(weeks=2)),
                        and_(
                            WikibaseConnectivityObservationModel.returned_data,
                            WikibaseConnectivityObservationModel.observation_date
                            > (datetime.now(tz=timezone.utc) - timedelta(weeks=3)),
                        ),
                    )
                )
            ),
        )
    )

    return query


async def get_wikibase_list_with_out_of_date_connectivity_observations() -> (
    list[WikibaseModel]
):
    """Get List of Wikibases with Out of Date Connectivity Observations"""

    return await get_wikibase_list(
        get_wikibase_with_out_of_date_connectivity_obs_query()
    )


def get_wikibase_with_out_of_date_log_first_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Log (First Month) Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            not_(
                WikibaseModel.log_month_observations.any(
                    and_(
                        WikibaseLogMonthObservationModel.first_month,
                        or_(
                            WikibaseLogMonthObservationModel.observation_date
                            > (datetime.now(tz=timezone.utc) - timedelta(weeks=40)),
                            and_(
                                WikibaseLogMonthObservationModel.returned_data,
                                WikibaseLogMonthObservationModel.observation_date
                                > (datetime.now(tz=timezone.utc) - timedelta(weeks=52)),
                            ),
                        ),
                    )
                )
            ),
        )
    )

    return query


async def get_wikibase_list_with_out_of_date_log_first_observations() -> (
    list[WikibaseModel]
):
    """Get List of Wikibases with Out of Date Log (First Month) Observations"""

    return await get_wikibase_list(get_wikibase_with_out_of_date_log_first_obs_query())


def get_wikibase_with_out_of_date_log_last_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Log (Last Month) Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            not_(
                WikibaseModel.log_month_observations.any(
                    and_(
                        not_(WikibaseLogMonthObservationModel.first_month),
                        or_(
                            WikibaseLogMonthObservationModel.observation_date
                            > (datetime.now(tz=timezone.utc) - timedelta(weeks=2)),
                            and_(
                                WikibaseLogMonthObservationModel.returned_data,
                                WikibaseLogMonthObservationModel.observation_date
                                > (datetime.now(tz=timezone.utc) - timedelta(weeks=3)),
                            ),
                        ),
                    )
                )
            ),
        )
    )

    return query


async def get_wikibase_list_with_out_of_date_log_last_observations() -> (
    list[WikibaseModel]
):
    """Get List of Wikibases with Out of Date Log (Last Month) Observations"""

    return await get_wikibase_list(get_wikibase_with_out_of_date_log_last_obs_query())


def get_wikibase_with_out_of_date_property_popularity_obs_query() -> (
    Select[tuple[WikibaseModel]]
):
    """Query Wikibases with Out of Date Property Popularity Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            not_(
                WikibaseModel.property_popularity_observations.any(
                    or_(
                        WikibasePropertyPopularityObservationModel.observation_date
                        > (datetime.now(tz=timezone.utc) - timedelta(weeks=2)),
                        and_(
                            WikibasePropertyPopularityObservationModel.returned_data,
                            WikibasePropertyPopularityObservationModel.observation_date
                            > (datetime.now(tz=timezone.utc) - timedelta(weeks=3)),
                        ),
                    )
                )
            ),
        )
    )

    return query


async def get_wikibase_list_with_out_of_date_property_popularity_observations() -> (
    list[WikibaseModel]
):
    """Get List of Wikibases with Out of Date Property Popularity Observations"""

    return await get_wikibase_list(
        get_wikibase_with_out_of_date_property_popularity_obs_query()
    )


def get_wikibase_with_out_of_date_quantity_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Quantity Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            not_(
                WikibaseModel.quantity_observations.any(
                    or_(
                        WikibaseQuantityObservationModel.observation_date
                        > (datetime.now(tz=timezone.utc) - timedelta(weeks=2)),
                        and_(
                            WikibaseQuantityObservationModel.returned_data,
                            WikibaseQuantityObservationModel.observation_date
                            > (datetime.now(tz=timezone.utc) - timedelta(weeks=3)),
                        ),
                    )
                )
            ),
        )
    )

    return query


async def get_wikibase_list_with_out_of_date_quantity_observations() -> (
    list[WikibaseModel]
):
    """Get List of Wikibases with Out of Date Quantity Observations"""

    return await get_wikibase_list(get_wikibase_with_out_of_date_quantity_obs_query())


def get_wikibase_with_out_of_date_software_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Software Version Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            not_(
                WikibaseModel.software_version_observations.any(
                    or_(
                        WikibaseSoftwareVersionObservationModel.observation_date
                        > (datetime.now(tz=timezone.utc) - timedelta(weeks=2)),
                        and_(
                            WikibaseSoftwareVersionObservationModel.returned_data,
                            WikibaseSoftwareVersionObservationModel.observation_date
                            > (datetime.now(tz=timezone.utc) - timedelta(weeks=3)),
                        ),
                    )
                )
            ),
        )
    )

    return query


async def get_wikibase_list_with_out_of_date_software_observations() -> (
    list[WikibaseModel]
):
    """Get List of Wikibases with Out of Date Software Version Observations"""

    return await get_wikibase_list(get_wikibase_with_out_of_date_software_obs_query())


def get_wikibase_with_out_of_date_stats_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Special:Statistics Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            not_(
                WikibaseModel.statistics_observations.any(
                    or_(
                        WikibaseStatisticsObservationModel.observation_date
                        > (datetime.now(tz=timezone.utc) - timedelta(weeks=2)),
                        and_(
                            WikibaseStatisticsObservationModel.returned_data,
                            WikibaseStatisticsObservationModel.observation_date
                            > (datetime.now(tz=timezone.utc) - timedelta(weeks=3)),
                        ),
                    )
                )
            ),
        )
    )

    return query


async def get_wikibase_list_with_out_of_date_stats_observations() -> (
    list[WikibaseModel]
):
    """Get List of Wikibases with Out of Date Special:Statistics Observations"""

    return await get_wikibase_list(get_wikibase_with_out_of_date_stats_obs_query())


def get_wikibase_with_out_of_date_user_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date User Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            not_(
                WikibaseModel.user_observations.any(
                    or_(
                        WikibaseUserObservationModel.observation_date
                        > (datetime.now(tz=timezone.utc) - timedelta(weeks=2)),
                        and_(
                            WikibaseUserObservationModel.returned_data,
                            WikibaseUserObservationModel.observation_date
                            > (datetime.now(tz=timezone.utc) - timedelta(weeks=3)),
                        ),
                    )
                )
            ),
        )
    )

    return query


async def get_wikibase_list_with_out_of_date_user_observations() -> list[WikibaseModel]:
    """Get List of Wikibases with Out of Date User Observations"""

    return await get_wikibase_list(get_wikibase_with_out_of_date_user_obs_query())