"""Get Aggregate Property Popularity"""

from typing import List

from sqlalchemy import select

from data.database_connection import get_async_session
from model.database import WikibaseModel, WikibasePropertyPopularityObservationModel
from model.strawberry.output import (
    WikibasePropertyPopularityAggregateCountStrawberryModel,
    WikibaseStrawberryModel,
)


async def get_aggregate_property_popularity() -> List[
    WikibasePropertyPopularityAggregateCountStrawberryModel
]:
    """Get Aggregate Property Popularity"""

    async with get_async_session() as async_session:
        wikibases = (
            await async_session.scalars(
                select(WikibaseModel).where(
                    WikibaseModel.property_popularity_observations.any(
                        WikibasePropertyPopularityObservationModel.returned_data
                    )
                )
            )
        ).all()

        wikibase_strawberries = [WikibaseStrawberryModel.marshal(c) for c in wikibases]

        property_dict: dict[
            str, WikibasePropertyPopularityAggregateCountStrawberryModel
        ] = {}

        for wikibase_strawberry in wikibase_strawberries:
            if (
                most_recent := wikibase_strawberry.property_popularity_observations.most_recent
            ) is not None:
                for property_count in most_recent.property_popularity_counts:
                    if property_count.property_url not in property_dict:
                        property_dict[
                            property_count.property_url
                        ] = WikibasePropertyPopularityAggregateCountStrawberryModel(
                            id=property_count.id,
                            property_url=property_count.property_url,
                        )
                    property_dict[
                        property_count.property_url
                    ].usage_count += property_count.usage_count
                    property_dict[property_count.property_url].wikibase_count += 1
        return sorted(property_dict.values(), key=lambda x: x.usage_count, reverse=True)
