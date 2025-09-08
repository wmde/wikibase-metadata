"""Get Out of Date Wikibase Queries"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import Select, and_, not_, or_
from fetch_data.bulk.get_wikibase_query import (
    get_connectivity_obs_wikibases_query,
    get_log_obs_wikibases_query,
    get_property_popularity_obs_wikibases_query,
    get_quantity_obs_wikibases_query,
    get_recent_changes_obs_wikibases_query,
    get_software_obs_wikibases_query,
    get_stats_obs_wikibases_query,
    get_time_to_first_value_obs_wikibases_query,
    get_user_obs_wikibases_query,
)
from model.database import (
    WikibaseConnectivityObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseRecentChangesObservationModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseStatisticsObservationModel,
    WikibaseTimeToFirstValueObservationModel,
    WikibaseUserObservationModel,
)


SAFE_HOUR_MARGIN = -6


def get_wikibase_with_out_of_date_connectivity_obs_query() -> (
    Select[tuple[WikibaseModel]]
):
    """Query Wikibases with Out of Date Connectivity Observations"""

    base_query = get_connectivity_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.connectivity_observations.any(
                or_(
                    WikibaseConnectivityObservationModel.observation_date
                    > (
                        datetime.now(tz=timezone.utc)
                        - timedelta(weeks=1, hours=SAFE_HOUR_MARGIN)
                    ),
                    and_(
                        WikibaseConnectivityObservationModel.returned_data,
                        WikibaseConnectivityObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=4, hours=SAFE_HOUR_MARGIN)
                        ),
                    ),
                )
            )
        )
    )

    return query


def get_wikibase_with_out_of_date_log_first_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Log (First Month) Observations"""

    base_query = get_log_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.log_month_observations.any(
                and_(
                    WikibaseLogMonthObservationModel.first_month,
                    or_(
                        WikibaseLogMonthObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=40, hours=SAFE_HOUR_MARGIN)
                        ),
                        and_(
                            WikibaseLogMonthObservationModel.returned_data,
                            WikibaseLogMonthObservationModel.observation_date
                            > (
                                datetime.now(tz=timezone.utc)
                                - timedelta(weeks=52, hours=SAFE_HOUR_MARGIN)
                            ),
                        ),
                    ),
                )
            )
        )
    )

    return query


def get_wikibase_with_out_of_date_log_last_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Log (Last Month) Observations"""

    base_query = get_log_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.log_month_observations.any(
                and_(
                    not_(WikibaseLogMonthObservationModel.first_month),
                    or_(
                        WikibaseLogMonthObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=1, hours=SAFE_HOUR_MARGIN)
                        ),
                        and_(
                            WikibaseLogMonthObservationModel.returned_data,
                            WikibaseLogMonthObservationModel.observation_date
                            > (
                                datetime.now(tz=timezone.utc)
                                - timedelta(weeks=4, hours=SAFE_HOUR_MARGIN)
                            ),
                        ),
                    ),
                )
            )
        )
    )

    return query


def get_wikibase_with_out_of_date_property_popularity_obs_query() -> (
    Select[tuple[WikibaseModel]]
):
    """Query Wikibases with Out of Date Property Popularity Observations"""

    base_query = get_property_popularity_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.property_popularity_observations.any(
                or_(
                    WikibasePropertyPopularityObservationModel.observation_date
                    > (
                        datetime.now(tz=timezone.utc)
                        - timedelta(weeks=1, hours=SAFE_HOUR_MARGIN)
                    ),
                    and_(
                        WikibasePropertyPopularityObservationModel.returned_data,
                        WikibasePropertyPopularityObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=4, hours=SAFE_HOUR_MARGIN)
                        ),
                    ),
                )
            ),
        )
    )

    return query


def get_wikibase_with_out_of_date_quantity_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Quantity Observations"""

    base_query = get_quantity_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.quantity_observations.any(
                or_(
                    WikibaseQuantityObservationModel.observation_date
                    > (
                        datetime.now(tz=timezone.utc)
                        - timedelta(weeks=1, hours=SAFE_HOUR_MARGIN)
                    ),
                    and_(
                        WikibaseQuantityObservationModel.returned_data,
                        WikibaseQuantityObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=4, hours=SAFE_HOUR_MARGIN)
                        ),
                    ),
                )
            )
        )
    )

    return query


def get_wikibase_with_out_of_date_recent_changes_obs_query() -> (
    Select[tuple[WikibaseModel]]
):
    """Query Wikibases with Out of Date Recent Changes Observations"""

    base_query = get_recent_changes_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.recent_changes_observations.any(
                or_(
                    WikibaseRecentChangesObservationModel.observation_date
                    > (
                        datetime.now(tz=timezone.utc)
                        - timedelta(weeks=1, hours=SAFE_HOUR_MARGIN)
                    ),
                    and_(
                        WikibaseRecentChangesObservationModel.returned_data,
                        WikibaseRecentChangesObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=4, hours=SAFE_HOUR_MARGIN)
                        ),
                    ),
                )
            )
        )
    )

    return query


def get_wikibase_with_out_of_date_software_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Software Version Observations"""

    base_query = get_software_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.software_version_observations.any(
                or_(
                    WikibaseSoftwareVersionObservationModel.observation_date
                    > (
                        datetime.now(tz=timezone.utc)
                        - timedelta(weeks=1, hours=SAFE_HOUR_MARGIN)
                    ),
                    and_(
                        WikibaseSoftwareVersionObservationModel.returned_data,
                        WikibaseSoftwareVersionObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=4, hours=SAFE_HOUR_MARGIN)
                        ),
                    ),
                )
            ),
        )
    )

    return query


def get_wikibase_with_out_of_date_stats_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date Special:Statistics Observations"""

    base_query = get_stats_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.statistics_observations.any(
                or_(
                    WikibaseStatisticsObservationModel.observation_date
                    > (
                        datetime.now(tz=timezone.utc)
                        - timedelta(weeks=1, hours=SAFE_HOUR_MARGIN)
                    ),
                    and_(
                        WikibaseStatisticsObservationModel.returned_data,
                        WikibaseStatisticsObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=4, hours=SAFE_HOUR_MARGIN)
                        ),
                    ),
                )
            )
        )
    )

    return query


def get_wikibase_with_out_of_date_time_to_first_value_obs_query() -> (
    Select[tuple[WikibaseModel]]
):
    """Query Wikibases with Out of Date Time to First Value Observations"""

    base_query = get_time_to_first_value_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.time_to_first_value_observations.any(
                or_(
                    WikibaseTimeToFirstValueObservationModel.observation_date
                    > (
                        datetime.now(tz=timezone.utc)
                        - timedelta(weeks=40, hours=SAFE_HOUR_MARGIN)
                    ),
                    and_(
                        WikibaseTimeToFirstValueObservationModel.returned_data,
                        WikibaseTimeToFirstValueObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=52, hours=SAFE_HOUR_MARGIN)
                        ),
                    ),
                )
            )
        )
    )

    return query


def get_wikibase_with_out_of_date_user_obs_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases with Out of Date User Observations"""

    base_query = get_user_obs_wikibases_query()
    query = base_query.where(
        not_(
            WikibaseModel.user_observations.any(
                or_(
                    WikibaseUserObservationModel.observation_date
                    > (
                        datetime.now(tz=timezone.utc)
                        - timedelta(weeks=1, hours=SAFE_HOUR_MARGIN)
                    ),
                    and_(
                        WikibaseUserObservationModel.returned_data,
                        WikibaseUserObservationModel.observation_date
                        > (
                            datetime.now(tz=timezone.utc)
                            - timedelta(weeks=4, hours=SAFE_HOUR_MARGIN)
                        ),
                    ),
                )
            )
        )
    )

    return query
