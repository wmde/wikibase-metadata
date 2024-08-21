"""Aggregate Statistics Strawberry Model"""

from typing import Optional
import strawberry

from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseStatisticsAggregateStrawberryModel:  # pylint: disable=too-many-instance-attributes
    """Aggregate Statistics"""

    total_pages: int = strawberry.field(description="Total Pages", graphql_type=BigInt)
    content_pages: int = strawberry.field(
        description="Content Pages", graphql_type=BigInt
    )
    total_files: int = strawberry.field(description="Total Files", graphql_type=BigInt)
    total_edits: int = strawberry.field(description="Total Edits", graphql_type=BigInt)
    content_page_word_count_total: int = strawberry.field(
        description="Total Content Word Count", graphql_type=BigInt
    )
    total_users: int = strawberry.field(description="Total Users", graphql_type=BigInt)
    active_users: int = strawberry.field(
        description="Active Users", graphql_type=BigInt
    )
    total_admin: int = strawberry.field(description="Total Admin", graphql_type=BigInt)
    wikibase_count: int = strawberry.field(description="Wikibases with Statistics Data")

    @strawberry.field(description="Content Page Word Count - Average")
    def content_page_word_count_avg(self) -> Optional[float]:
        """Average Word Count per Content Page"""

        if self.content_pages == 0:
            return None
        return self.content_page_word_count_total / self.content_pages

    @strawberry.field(description="Average Edits per Page")
    def edits_per_page_avg(self) -> Optional[float]:
        """Average Edits per Page"""

        if self.total_pages == 0:
            return None
        return self.total_edits / self.total_pages

    def __init__(  # pylint: disable=too-many-arguments
        self,
        total_pages: int,
        content_pages: int,
        total_files: int,
        total_edits: int,
        content_page_word_count_total: int,
        total_users: int,
        active_users: int,
        total_admin: int,
        wikibase_count: int,
    ) -> "WikibaseStatisticsAggregateStrawberryModel":
        self.wikibase_count = wikibase_count
        self.total_pages = total_pages
        self.content_pages = content_pages
        self.total_files = total_files
        self.total_edits = total_edits
        self.content_page_word_count_total = content_page_word_count_total
        self.total_users = total_users
        self.active_users = active_users
        self.total_admin = total_admin
