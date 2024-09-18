"""Wikibase Statistics Data Observation Strawberry Models"""

from typing import Optional
import strawberry

from model.database import WikibaseStatisticsObservationModel
from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseStatisticsPagesObservationStrawberryModel:
    """Wikibase Statistics Pages Data"""

    total_pages: int = strawberry.field(description="Total Pages", graphql_type=BigInt)
    content_pages: int = strawberry.field(
        description="Content Pages", graphql_type=BigInt
    )
    content_page_word_count_total: Optional[int] = strawberry.field(
        description="Content Page Word Count - Total", graphql_type=Optional[BigInt]
    )

    @strawberry.field(description="Content Page Word Count - Average")
    def content_page_word_count_avg(self) -> Optional[float]:
        """Average Word Count per Content Page"""

        if self.content_page_word_count_total is None or self.content_pages == 0:
            return None
        return self.content_page_word_count_total / self.content_pages

    @classmethod
    def marshal(
        cls, model: WikibaseStatisticsObservationModel
    ) -> "WikibaseStatisticsPagesObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if model.total_pages is None or model.content_pages is None:
            raise ValueError(
                f"Statistics Observation {model.id}: Expected totals when observation returned data"
            )
        return cls(
            total_pages=model.total_pages,
            content_pages=model.content_pages,
            content_page_word_count_total=model.content_page_word_count_total,
        )

    def __init__(
        self, total_pages: int, content_pages: int, content_page_word_count_total: int
    ) -> "WikibaseStatisticsPagesObservationStrawberryModel":
        self.total_pages = total_pages
        self.content_pages = content_pages
        self.content_page_word_count_total = content_page_word_count_total
