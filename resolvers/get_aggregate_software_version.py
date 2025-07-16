"""Get Aggregate Software Version"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import (
    WikibaseModel,
    WikibaseSoftwareModel,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
)
from model.enum import WikibaseSoftwareType
from model.strawberry.input import WikibaseTypeInput
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseSoftwareVersionAggregateStrawberryModel,
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel,
)


async def get_aggregate_version(
    software_type: WikibaseSoftwareType,
    page_number: PageNumberType,
    page_size: PageSizeType,
    wikibase_type: Optional[WikibaseTypeInput] = None,
) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
    """Get Aggregate Software Version"""

    query = get_query(software_type, wikibase_type)

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
                software_dict.values(),
                key=lambda x: (-x.wikibase_count(), x.software_name),
            )[page_size * (page_number - 1) : page_size * page_number],
        )


def get_query(
    software_type: WikibaseSoftwareType, wikibase_type: Optional[WikibaseTypeInput]
) -> Select[tuple[str, Optional[str], Optional[datetime], Optional[str], int]]:
    """Get Software Version Query"""

    rank_subquery = (
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
        .where(
            and_(
                WikibaseSoftwareVersionObservationModel.returned_data,
                WikibaseSoftwareVersionObservationModel.wikibase.has(
                    WikibaseModel.checked
                    if wikibase_type is None
                    else and_(
                        WikibaseModel.checked,
                        WikibaseModel.wikibase_type.in_(wikibase_type.include) if wikibase_type.include is not None else True,
                        WikibaseModel.wikibase_type.not_in(wikibase_type.exclude) if wikibase_type.exclude is not None else True,
                    )
                ),
            )
        )
        .subquery()
    )

    next_subquery = (
        select(
            WikibaseSoftwareVersionModel.version,
            WikibaseSoftwareVersionModel.version_date,
            WikibaseSoftwareVersionModel.version_hash,
            WikibaseSoftwareModel.software_name,
        )
        .join(WikibaseSoftwareModel)
        .join(
            rank_subquery,
            onclause=and_(
                WikibaseSoftwareVersionModel.wikibase_software_version_observation_id
                == rank_subquery.c.id,
                rank_subquery.c.rank == 1,
            ),
        )
        .where(WikibaseSoftwareModel.software_type == software_type)
        .subquery()
    )

    query = select(
        next_subquery.c.software_name,
        next_subquery.c.version,
        next_subquery.c.version_date,
        next_subquery.c.version_hash,
        # pylint: disable-next=not-callable
        func.count().label("wikibase_count"),
    ).group_by(
        next_subquery.c.software_name,
        next_subquery.c.version,
        next_subquery.c.version_date,
        next_subquery.c.version_hash,
    )
    return query
