"""Quantity CSV"""

from fastapi import BackgroundTasks
from sqlalchemy import and_, func, or_, select

from export_csv.util import export_csv
from model.database import (
    WikibaseModel,
    WikibaseQuantityObservationModel,
    WikibaseRecentChangesObservationModel,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseSoftwareModel,
)
from model.enum import WikibaseType


async def export_metric_csv(background_tasks: BackgroundTasks):
    """CSV with Requested Metrics"""

    query = get_metrics_query()

    return await export_csv(
        query=query,
        export_filename="metrics",
        index_col="wikibase_id",
        background_tasks=background_tasks,
    )


def get_metrics_query():
    """
    Filter Out Offline and Test Wikis

    Pull Quantity, Recent Changes, and Software Version Metrics
    """

    filtered_wikibase_subquery = (
        select(WikibaseModel)
        .where(
            and_(
                WikibaseModel.checked,
                or_(
                    # pylint: disable-next=singleton-comparison
                    WikibaseModel.wikibase_type == None,
                    and_(
                        # WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                        WikibaseModel.wikibase_type
                        != WikibaseType.TEST,
                    ),
                ),
            )
        )
        .cte(name="filtered_wikibases")
    )

    quantity_rank_subquery = (
        select(
            WikibaseQuantityObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseQuantityObservationModel.wikibase_id,
                order_by=WikibaseQuantityObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where((WikibaseQuantityObservationModel.returned_data))
        .subquery()
    )
    most_recent_successful_quantity_obs = (
        select(WikibaseQuantityObservationModel)
        .join(
            quantity_rank_subquery,
            onclause=and_(
                WikibaseQuantityObservationModel.id == quantity_rank_subquery.c.id,
                quantity_rank_subquery.c.rank == 1,
            ),
        )
        .cte(name="filtered_quantity_observations")
    )

    rc_rank_subquery = (
        select(
            WikibaseRecentChangesObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseRecentChangesObservationModel.wikibase_id,
                order_by=WikibaseRecentChangesObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where((WikibaseRecentChangesObservationModel.returned_data))
        .subquery()
    )
    most_recent_successful_rc_obs = (
        select(WikibaseRecentChangesObservationModel)
        .join(
            rc_rank_subquery,
            onclause=and_(
                WikibaseRecentChangesObservationModel.id == rc_rank_subquery.c.id,
                rc_rank_subquery.c.rank == 1,
            ),
        )
        .cte(name="filtered_recent_changes_observations")
    )

    sv_rank_subquery = (
        select(
            WikibaseSoftwareVersionObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseSoftwareVersionObservationModel.wikibase_id,
                order_by=WikibaseSoftwareVersionObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where((WikibaseSoftwareVersionObservationModel.returned_data))
        .subquery()
    )
    most_recent_successful_sv_obs = (
        select(
            WikibaseSoftwareVersionObservationModel.wikibase_id,
            WikibaseSoftwareVersionObservationModel.observation_date,
            WikibaseSoftwareVersionModel.version,
            WikibaseSoftwareModel.software_name,
        )
        .select_from(WikibaseSoftwareVersionObservationModel)
        .join(WikibaseSoftwareVersionModel)
        .join(WikibaseSoftwareModel)
        .join(
            sv_rank_subquery,
            onclause=and_(
                WikibaseSoftwareVersionObservationModel.id == sv_rank_subquery.c.id,
                sv_rank_subquery.c.rank == 1,
            ),
        )
        .where(WikibaseSoftwareModel.software_name == "MediaWiki")
        .cte(name="filtered_software_version_observations")
    )

    query = (
        select(
            filtered_wikibase_subquery.c.id.label("wikibase_id"),
            filtered_wikibase_subquery.c.wb_type.label("wikibase_type"),
            most_recent_successful_quantity_obs.c.date.label(
                "quantity_observation_date"
            ),
            most_recent_successful_quantity_obs.c.total_items,
            most_recent_successful_quantity_obs.c.total_lexemes,
            most_recent_successful_quantity_obs.c.total_properties,
            most_recent_successful_quantity_obs.c.total_triples,
            most_recent_successful_quantity_obs.c.total_external_identifier_properties.label(
                "total_ei_properties"
            ),
            most_recent_successful_quantity_obs.c.total_external_identifier_statements.label(
                "total_ei_statements"
            ),
            most_recent_successful_quantity_obs.c.total_url_properties,
            most_recent_successful_quantity_obs.c.total_url_statements,
            most_recent_successful_rc_obs.c.date.label(
                "recent_changes_observation_date"
            ),
            most_recent_successful_rc_obs.c.first_change_date,
            most_recent_successful_rc_obs.c.last_change_date,
            most_recent_successful_rc_obs.c.human_change_count,
            most_recent_successful_rc_obs.c.human_change_user_count,
            most_recent_successful_rc_obs.c.bot_change_count,
            most_recent_successful_rc_obs.c.bot_change_user_count,
            most_recent_successful_sv_obs.c.observation_date.label(
                "software_version_observation_date"
            ),
            most_recent_successful_sv_obs.c.software_name,
            most_recent_successful_sv_obs.c.version,
        )
        .join(
            most_recent_successful_quantity_obs,
            onclause=filtered_wikibase_subquery.c.id
            == most_recent_successful_quantity_obs.c.wikibase_id,
            isouter=True,
        )
        .join(
            most_recent_successful_rc_obs,
            onclause=filtered_wikibase_subquery.c.id
            == most_recent_successful_rc_obs.c.wikibase_id,
            isouter=True,
        )
        .join(
            most_recent_successful_sv_obs,
            onclause=filtered_wikibase_subquery.c.id
            == most_recent_successful_sv_obs.c.wikibase_id,
            isouter=True,
        )
    )

    return query
