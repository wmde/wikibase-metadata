"""Get Filtered Wikibase Query"""

import re
from typing import Optional

from sqlalchemy import Select, String, cast, or_, select

from model.database import WikibaseModel, WikibaseCategoryModel, WikibaseURLModel
from model.enum import WikibaseType
from model.strawberry.input import WikibaseFilterInput

ALLOWED_CHARACTERS = re.compile(r"[a-z0-9.\-_ ]+", re.IGNORECASE)
ONLY_ALLOWED_CHARACTERS = re.compile(r"^[a-z0-9.\-_ ]+$", re.IGNORECASE)


def get_filtered_wikibase_query(
    wikibase_filter: Optional[WikibaseFilterInput] = None,
) -> Select[tuple[WikibaseModel]]:
    """Filtered list of Wikibases"""

    query = select(WikibaseModel).where(WikibaseModel.checked)

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
                WikibaseModel.wikibase_name.like(
                    "%" + wikibase_filter.search_text + "%"
                ),
                WikibaseModel.url.has(
                    WikibaseURLModel.url.like("%" + wikibase_filter.search_text + "%")
                ),
                or_(
                    # pylint: disable-next=singleton-comparison
                    WikibaseModel.category_id == None,
                    WikibaseModel.category.has(
                        cast(WikibaseCategoryModel.category, String).like(
                            "%" + wikibase_filter.search_text.replace(" ", "_") + "%"
                        )
                    ),
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
