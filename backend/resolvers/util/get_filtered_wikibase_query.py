# pylint: disable=too-many-branches

"""Get Filtered Wikibase Query"""

import re
from typing import Optional

from sqlalchemy import Select, String, cast, or_, select
from sqlalchemy.orm import selectinload

from model.database import WikibaseModel, WikibaseCategoryModel, WikibaseURLModel
from model.enum import WikibaseType
from model.strawberry.input import WikibaseFilterInput

ALLOWED_CHARACTERS = re.compile(r"[a-z0-9.\-_ ]+", re.IGNORECASE)
ONLY_ALLOWED_CHARACTERS = re.compile(r"^[a-z0-9.\-_ ]+$", re.IGNORECASE)


def get_filtered_wikibase_query(
    wikibase_filter: Optional[WikibaseFilterInput] = None,
    fields: Optional[list[str]] = None,
) -> Select[tuple[WikibaseModel]]:
    """Filtered list of Wikibases"""

    query = select(WikibaseModel).where(WikibaseModel.checked)

    if fields is not None:
        if "connectivityObservations" in fields:
            query = query.options(selectinload(WikibaseModel.connectivity_observations))
        if "externalIdentifierObservations" in fields:
            query = query.options(
                selectinload(WikibaseModel.external_identifier_observations)
            )
        if "logObservations" in fields:
            query = query.options(selectinload(WikibaseModel.log_month_observations))
        if "propertyPopularityObservations" in fields:
            query = query.options(
                selectinload(WikibaseModel.property_popularity_observations)
            )
        if "quantityObservations" in fields:
            query = query.options(selectinload(WikibaseModel.quantity_observations))
        if "recentChangesObservations" in fields:
            query = query.options(
                selectinload(WikibaseModel.recent_changes_observations)
            )
        if "softwareVersionObservations" in fields:
            query = query.options(
                selectinload(WikibaseModel.software_version_observations)
            )
        if "statisticsObservations" in fields:
            query = query.options(
                selectinload(WikibaseModel.software_version_observations)
            )
        if "timeToFirstValueObservations" in fields:
            query = query.options(
                selectinload(WikibaseModel.time_to_first_value_observations)
            )
        if "userObservations" in fields:
            query = query.options(selectinload(WikibaseModel.user_observations))

    if wikibase_filter is None:
        return query.where(WikibaseModel.reuse)

    if not wikibase_filter.ignore_reuse:
        query = query.where(WikibaseModel.reuse)

    if wikibase_filter.search_text is not None and len(wikibase_filter.search_text) > 0:
        if not ONLY_ALLOWED_CHARACTERS.match(wikibase_filter.search_text):
            disallowed_characters = ALLOWED_CHARACTERS.sub(
                r"", wikibase_filter.search_text
            )
            raise ValueError(f"Disallowed Characters: {disallowed_characters}")
        query = query.where(
            or_(
                WikibaseModel.wikibase_name.ilike(
                    "%" + wikibase_filter.search_text + "%"
                ),
                WikibaseModel.url.has(
                    WikibaseURLModel.url.ilike("%" + wikibase_filter.search_text + "%")
                ),
                WikibaseModel.category.has(
                    cast(WikibaseCategoryModel.category, String).like(
                        "%"
                        + wikibase_filter.search_text.replace(" ", "_").upper()
                        + "%"
                    )
                ),
            )
        )

    if wikibase_filter.wikibase_type is not None:
        if (
            wikibase_filter.wikibase_type.exclude is not None
            and len(wikibase_filter.wikibase_type.exclude) > 0
        ):
            if WikibaseType.UNKNOWN in wikibase_filter.wikibase_type.exclude:
                query = query.where(
                    WikibaseModel.wikibase_type.notin_(
                        wikibase_filter.wikibase_type.exclude
                    )
                )
            else:
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
            if WikibaseType.UNKNOWN in wikibase_filter.wikibase_type.include:
                query = query.where(
                    or_(
                        # pylint: disable-next=singleton-comparison
                        WikibaseModel.wikibase_type == None,
                        WikibaseModel.wikibase_type.in_(
                            wikibase_filter.wikibase_type.include
                        ),
                    )
                )
            else:
                query = query.where(
                    WikibaseModel.wikibase_type.in_(
                        wikibase_filter.wikibase_type.include
                    )
                )

    return query
