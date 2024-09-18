"""Wikibase Statistics Data Observation Strawberry Models"""

from typing import Optional
import strawberry

from model.database import WikibaseStatisticsObservationModel
from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseStatisticsFilesObservationStrawberryModel:
    """Wikibase Statistics Files Data"""

    total_files: Optional[int] = strawberry.field(
        description="Total Files", graphql_type=Optional[BigInt]
    )

    @classmethod
    def marshal(
        cls, model: WikibaseStatisticsObservationModel
    ) -> "WikibaseStatisticsFilesObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(total_files=model.total_files)

    def __init__(
        self, total_files: int
    ) -> "WikibaseStatisticsFilesObservationStrawberryModel":
        self.total_files = total_files
