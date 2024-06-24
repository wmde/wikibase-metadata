"""Wikibase Property Popularity Count"""

import strawberry

from model.database import WikibasePropertyPopularityCountModel


@strawberry.type
class WikibasePropertyPopularityCountStrawberryModel:
    """Wikibase Property Popularity Count"""

    id: strawberry.ID
    property_url: str = strawberry.field(description="Property URL")
    usage_count: int = strawberry.field(
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
