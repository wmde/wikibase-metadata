"""Get Wikibase Queries"""

from sqlalchemy import Select, and_, or_, select
from model.database import (
    WikibaseModel,
    WikibaseURLModel,
)
from model.enum import WikibaseType


def get_connectivity_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have Connectivity Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                and_(
                    WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                    WikibaseModel.wikibase_type != WikibaseType.TEST,
                ),
            ),
            WikibaseModel.sparql_endpoint_url.has(WikibaseURLModel.id),
        )
    )

    return query


def get_external_identifier_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have External Identifier Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                WikibaseModel.wikibase_type != WikibaseType.TEST,
            ),
            WikibaseModel.sparql_endpoint_url.has(WikibaseURLModel.id),
        )
    )

    return query


def get_log_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have Log Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                and_(
                    WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                    WikibaseModel.wikibase_type != WikibaseType.TEST,
                ),
            ),
            WikibaseModel.script_path.has(WikibaseURLModel.id),
        )
    )

    return query


def get_property_popularity_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have Property Popularity Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                and_(
                    WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                    WikibaseModel.wikibase_type != WikibaseType.TEST,
                ),
            ),
            WikibaseModel.sparql_endpoint_url.has(WikibaseURLModel.id),
        )
    )

    return query


def get_quantity_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have Quantity Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                WikibaseModel.wikibase_type != WikibaseType.TEST,
            ),
            WikibaseModel.sparql_endpoint_url.has(WikibaseURLModel.id),
        )
    )

    return query


def get_recent_changes_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have Recent Changes Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                and_(
                    WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                    WikibaseModel.wikibase_type != WikibaseType.TEST,
                ),
            ),
            WikibaseModel.script_path.has(WikibaseURLModel.id),
        )
    )

    return query


def get_software_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have Software Version Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                and_(
                    WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                    WikibaseModel.wikibase_type != WikibaseType.TEST,
                ),
            ),
            WikibaseModel.article_path.has(WikibaseURLModel.id),
        )
    )

    return query


def get_stats_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have Special:Statistics Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                and_(
                    WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                    WikibaseModel.wikibase_type != WikibaseType.TEST,
                ),
            ),
            WikibaseModel.article_path.has(WikibaseURLModel.id),
        )
    )

    return query


def get_time_to_first_value_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have Time to First Value Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                and_(
                    # WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                    WikibaseModel.wikibase_type != WikibaseType.TEST,
                ),
            ),
            WikibaseModel.script_path.has(WikibaseURLModel.id),
        )
    )

    return query


def get_user_obs_wikibases_query() -> Select[tuple[WikibaseModel]]:
    """Query Wikibases that Can Have User Observations"""

    query = select(WikibaseModel).where(
        and_(
            WikibaseModel.checked,
            or_(
                # pylint: disable-next=singleton-comparison
                WikibaseModel.wikibase_type == None,
                and_(
                    WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                    WikibaseModel.wikibase_type != WikibaseType.TEST,
                ),
            ),
            WikibaseModel.script_path.has(WikibaseURLModel.id),
        )
    )

    return query
