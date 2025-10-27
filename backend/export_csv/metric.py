"""Metrics CSV"""

from fastapi.responses import StreamingResponse
from sqlalchemy import Select, and_, func, or_, select

from export_csv.util import export_csv
from model.database import (
    WikibaseExternalIdentifierObservationModel,
    WikibaseModel,
    WikibaseQuantityObservationModel,
    WikibaseRecentChangesObservationModel,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseSoftwareModel,
    WikibaseURLModel,
)
from model.enum import WikibaseType, WikibaseURLType


async def export_metric_csv() -> StreamingResponse:
    """CSV with Requested Metrics"""

    query = get_metrics_query()

    return await export_csv(
        query=query,
        export_filename="metrics",
        index_col="wikibase_id",
    )


def get_metrics_query() -> Select:
    """
    Filter Out Offline and Test Wikis

    Pull Quantity, External Identifier, Recent Changes, and Software Version Metrics
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

    external_identifier_rank_subquery = (
        select(
            WikibaseExternalIdentifierObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseExternalIdentifierObservationModel.wikibase_id,
                order_by=[
                    WikibaseExternalIdentifierObservationModel.observation_date.desc(),
                    WikibaseExternalIdentifierObservationModel.id,
                ],
            )
            .label("rank"),
        )
        .where((WikibaseExternalIdentifierObservationModel.returned_data))
        .subquery()
    )
    most_recent_successful_ei_obs = (
        select(WikibaseExternalIdentifierObservationModel)
        .join(
            external_identifier_rank_subquery,
            onclause=and_(
                WikibaseExternalIdentifierObservationModel.id
                == external_identifier_rank_subquery.c.id,
                external_identifier_rank_subquery.c.rank == 1,
            ),
        )
        .cte(name="filtered_external_identifier_observations")
    )

    quantity_rank_subquery = (
        select(
            WikibaseQuantityObservationModel.id,
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
                order_by=[
                    WikibaseRecentChangesObservationModel.observation_date.desc(),
                    WikibaseRecentChangesObservationModel.id,
                ],
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
                order_by=[
                    WikibaseSoftwareVersionObservationModel.observation_date.desc(),
                    WikibaseSoftwareVersionObservationModel.id,
                ],
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
            WikibaseURLModel.url.label("base_url"),
            most_recent_successful_quantity_obs.c.date.label(
                "quantity_observation_date"
            ),
            most_recent_successful_quantity_obs.c.total_items,
            most_recent_successful_quantity_obs.c.total_lexemes,
            most_recent_successful_quantity_obs.c.total_properties,
            most_recent_successful_quantity_obs.c.total_triples,
            most_recent_successful_ei_obs.c.date.label("ei_observation_date"),
            most_recent_successful_ei_obs.c.total_external_identifier_properties.label(
                "total_ei_properties"
            ),
            most_recent_successful_ei_obs.c.total_external_identifier_statements.label(
                "total_ei_statements"
            ),
            most_recent_successful_ei_obs.c.total_url_properties,
            most_recent_successful_ei_obs.c.total_url_statements,
            most_recent_successful_rc_obs.c.date.label(
                "recent_changes_observation_date"
            ),
            most_recent_successful_rc_obs.c.first_change_date,
            most_recent_successful_rc_obs.c.last_change_date,
            most_recent_successful_rc_obs.c.human_change_count,
            most_recent_successful_rc_obs.c.human_change_user_count,
            most_recent_successful_rc_obs.c.human_change_user_count_five_plus.label(
                "human_change_active_user_count"
            ),
            most_recent_successful_rc_obs.c.bot_change_count,
            most_recent_successful_rc_obs.c.bot_change_user_count,
            most_recent_successful_rc_obs.c.bot_change_user_count_five_plus.label(
                "bot_change_active_user_count"
            ),
            most_recent_successful_sv_obs.c.observation_date.label(
                "software_version_observation_date"
            ),
            most_recent_successful_sv_obs.c.software_name,
            most_recent_successful_sv_obs.c.version,
        )
        .join(
            WikibaseURLModel,
            onclause=and_(
                filtered_wikibase_subquery.c.id == WikibaseURLModel.wikibase_id,
                WikibaseURLModel.url_type == WikibaseURLType.BASE_URL,
            ),
        )
        .join(
            most_recent_successful_quantity_obs,
            onclause=filtered_wikibase_subquery.c.id
            == most_recent_successful_quantity_obs.c.wikibase_id,
            isouter=True,
        )
        .join(
            most_recent_successful_ei_obs,
            onclause=filtered_wikibase_subquery.c.id
            == most_recent_successful_ei_obs.c.wikibase_id,
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
