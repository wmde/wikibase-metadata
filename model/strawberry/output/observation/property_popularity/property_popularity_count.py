"""Wikibase Property Popularity Count"""

from typing import Union
import strawberry

from model.database import WikibasePropertyPopularityCountModel



# This is needed because GraphQL does not support 64 bit integers
BigInt = strawberry.scalar(
    Union[int, str],  # type: ignore
    serialize=lambda v: int(v),
    parse_value=lambda v: str(v),
    description="BigInt field",
)
 
@strawberry.type
class WikibasePropertyPopularityCountStrawberryModel:
    """Wikibase Property Popularity Count"""

    id: strawberry.ID
    property_url: str = strawberry.field(description="Property URL")
    usage_count = strawberry.field(graphql_type=BigInt,
        description="Number of Triples with this Property"
    )

    @classmethod
    def marshal(
        cls, model: WikibasePropertyPopularityCountModel
    ) -> "WikibasePropertyPopularityCountStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            property_url=model.property_url,
            usage_count=model.usage_count,
        )
