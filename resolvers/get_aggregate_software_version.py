"""Get Aggregate Property Popularity"""

from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy import Select, and_, select, func

from data.database_connection import get_async_session
from model.database import (
    WikibaseSoftwareTypes,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
)
from model.strawberry.output import (
    Page,
    WikibaseSoftwareVersionAggregateStrawberryModel,
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel,
)


async def get_aggregate_version(
    software_type: WikibaseSoftwareTypes, page_number: int, page_size: int
) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
    """Get Aggregate Property Popularity"""

    query = get_query(software_type)

    async with get_async_session() as async_session:
        results = (await async_session.execute(query)).all()

        software_dict: dict[
            str, WikibaseSoftwareVersionDoubleAggregateStrawberryModel
        ] = {}
        for r in results:
            if r[1] not in software_dict:
                software_dict[
                    r[1]
                ] = WikibaseSoftwareVersionDoubleAggregateStrawberryModel(
                    r[0], r[1], []
                )
            software_dict[r[1]]._versions.append(
                WikibaseSoftwareVersionAggregateStrawberryModel(
                    r[0], r[2], r[3], r[4], r[5]
                )
            )

        return Page.marshal(
            page_number,
            page_size,
            len(software_dict),
            sorted(
                software_dict.values(), key=lambda x: x.wikibase_count(), reverse=True
            )[page_size * (page_number - 1) : page_size * page_number],
        )


def get_query(
    software_type: WikibaseSoftwareTypes,
) -> Select[Tuple[int, str, Optional[str], Optional[datetime], Optional[str], int]]:
    rank_subquery = (
        select(
            WikibaseSoftwareVersionObservationModel,
            func.rank()
            .over(
                partition_by=WikibaseSoftwareVersionObservationModel.wikibase_id,
                order_by=WikibaseSoftwareVersionObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(WikibaseSoftwareVersionObservationModel.returned_data)
        .subquery()
    )
    query = (
        select(
            func.min(WikibaseSoftwareVersionModel.id).label("id"),
            WikibaseSoftwareVersionModel.software_name,
            WikibaseSoftwareVersionModel.version,
            WikibaseSoftwareVersionModel.version_date,
            WikibaseSoftwareVersionModel.version_hash,
            func.count().label("wikibase_count"),
        )
        .join(rank_subquery)
        .where(
            and_(
                rank_subquery.c.rank == 1,
                WikibaseSoftwareVersionModel.software_type == software_type,
            )
        )
        .group_by(
            WikibaseSoftwareVersionModel.software_name,
            WikibaseSoftwareVersionModel.version,
            WikibaseSoftwareVersionModel.version_date,
            WikibaseSoftwareVersionModel.version_hash,
        )
        .order_by("id")
    )
    return query