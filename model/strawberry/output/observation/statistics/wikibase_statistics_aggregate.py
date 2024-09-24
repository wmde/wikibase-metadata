"""Aggregate Statistics Strawberry Model"""

import strawberry

from model.strawberry.output.observation.statistics.component import (
    WikibaseStatisticsEditsObservationStrawberryModel,
    WikibaseStatisticsFilesObservationStrawberryModel,
    WikibaseStatisticsPagesObservationStrawberryModel,
    WikibaseStatisticsUsersObservationStrawberryModel,
)


@strawberry.type
class WikibaseStatisticsAggregateStrawberryModel:
    """Aggregate Statistics"""

    edits: WikibaseStatisticsEditsObservationStrawberryModel
    files: WikibaseStatisticsFilesObservationStrawberryModel
    pages: WikibaseStatisticsPagesObservationStrawberryModel
    users: WikibaseStatisticsUsersObservationStrawberryModel

    wikibase_count: int = strawberry.field(description="Wikibases with Statistics Data")

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
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
        self.edits = WikibaseStatisticsEditsObservationStrawberryModel(
            total_edits, total_pages
        )
        self.files = WikibaseStatisticsFilesObservationStrawberryModel(total_files)
        self.pages = WikibaseStatisticsPagesObservationStrawberryModel(
            total_pages, content_pages, content_page_word_count_total
        )
        self.users = WikibaseStatisticsUsersObservationStrawberryModel(
            total_users, active_users, total_admin
        )
        self.wikibase_count = wikibase_count
