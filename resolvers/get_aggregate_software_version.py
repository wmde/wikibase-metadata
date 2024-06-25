"""Get Aggregate Property Popularity"""

from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import Select, and_, select, func

from data.database_connection import get_async_session
from model.database import (
    WikibaseSoftwareTypes,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
)
from model.strawberry.output import (
    WikibaseSoftwareVersionAggregateStrawberryModel,
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel,
)


async def get_aggregate_extension_version() -> List[
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel
]:
    return await get_aggregate_version(WikibaseSoftwareTypes.extension)


async def get_aggregate_library_version() -> List[
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel
]:
    return await get_aggregate_version(WikibaseSoftwareTypes.library)


async def get_aggregate_skin_version() -> List[
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel
]:
    return await get_aggregate_version(WikibaseSoftwareTypes.skin)


async def get_aggregate_software_version() -> List[
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel
]:
    return await get_aggregate_version(WikibaseSoftwareTypes.software)


async def get_aggregate_version(
    software_type: WikibaseSoftwareTypes,
) -> List[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
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

        return sorted(
            software_dict.values(), key=lambda x: x.wikibase_count(), reverse=True
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
