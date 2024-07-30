"""Wikibase Location Strawberry Model"""

from typing import Optional
import strawberry

from model.database import WikibaseModel


@strawberry.type
class WikibaseLocationStrawberryModel:
    """Wikibase Location"""

    country: Optional[str] = strawberry.field(description="Country")
    region: str = strawberry.field(description="Region")

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseLocationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(country=model.country, region=model.region)
