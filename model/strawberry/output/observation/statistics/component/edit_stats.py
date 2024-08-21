"""Wikibase Statistics Data Observation Strawberry Models"""

from typing import Optional
import strawberry

from model.database import WikibaseStatisticsObservationModel
from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseStatisticsEditsObservationStrawberryModel:
    """Wikibase Statistics Edits Data"""

    total_edits: int = strawberry.field(description="Total Edits", graphql_type=BigInt)
    total_pages: strawberry.Private[int]

    @strawberry.field(description="Average Edits per Page")
    def edits_per_page_avg(self) -> Optional[float]:
        """Average Edits per Page"""

        if self.total_pages == 0:
            return None
        return self.total_edits / self.total_pages

    @classmethod
    def marshal(
        cls, model: WikibaseStatisticsObservationModel
    ) -> "WikibaseStatisticsEditsObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if model.total_edits is None or model.total_pages is None:
            raise ValueError(
                f"Statistics Observation {model.id}: Expected totals when observation returned data"
            )
        return cls(total_edits=model.total_edits, total_pages=model.total_pages)

    def __init__(
        self, total_edits: int, total_pages: int
    ) -> "WikibaseStatisticsEditsObservationStrawberryModel":
        self.total_edits = total_edits
        self.total_pages = total_pages
