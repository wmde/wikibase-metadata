"""Get Aggregate Property Popularity"""

from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import (
    WikibaseModel,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
)
from model.enum import WikibaseSoftwareTypes
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
        for (
            software_name,
            version,
            version_date,
            version_hash,
            wikibase_count,
        ) in results:
            if software_name not in software_dict:
                software_dict[software_name] = (
                    WikibaseSoftwareVersionDoubleAggregateStrawberryModel(
                        software_name=software_name, versions=[]
                    )
                )
            software_dict[software_name].private_versions.append(
                WikibaseSoftwareVersionAggregateStrawberryModel(
                    version=version,
                    version_date=version_date,
                    version_hash=version_hash,
                    wikibase_count=wikibase_count,
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
) -> Select[Tuple[str, Optional[str], Optional[datetime], Optional[str], int]]:
    """Get Software Version Query"""

    rank_subquery = (
        select(
            WikibaseSoftwareVersionObservationModel,
            func.rank()  # pylint: disable=not-callable
            .over(
                partition_by=WikibaseSoftwareVersionObservationModel.wikibase_id,
                order_by=WikibaseSoftwareVersionObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(
            and_(
                WikibaseSoftwareVersionObservationModel.returned_data,
                WikibaseSoftwareVersionObservationModel.wikibase.has(
                    WikibaseModel.checked
                ),
            )
        )
        .subquery()
    )
    query = (
        select(
            WikibaseSoftwareVersionModel.software_name,
            WikibaseSoftwareVersionModel.version,
            WikibaseSoftwareVersionModel.version_date,
            WikibaseSoftwareVersionModel.version_hash,
            func.count().label("wikibase_count"),  # pylint: disable=not-callable
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
