"""Wikibase Statistics Data Observation Strawberry Models"""

from typing import Optional
import strawberry

from model.database import WikibaseStatisticsObservationModel
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseStatisticsEditsObservationStrawberryModel:
    """Wikibase Statistics Edits Data"""

    total_edits: int = strawberry.field(description="Total Edits", graphql_type=BigInt)

    total_pages: strawberry.Private[int]

    @strawberry.field(description="Average Edits per Page")
    def edits_per_page(self) -> Optional[float]:
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


@strawberry.type
class WikibaseStatisticsPagesObservationStrawberryModel:
    """Wikibase Statistics Pages Data"""

    total_pages: int = strawberry.field(description="Total Pages", graphql_type=BigInt)
    content_pages: int = strawberry.field(
        description="Content Pages", graphql_type=BigInt
    )
    content_pages_word_count_total: Optional[int] = strawberry.field(
        description="Total Words in Content Pages", graphql_type=Optional[BigInt]
    )

    @strawberry.field(description="Average Word Count per Content Page")
    def content_pages_word_count_avg(self) -> Optional[float]:
        """Average Word Count per Content Page"""
        if self.content_pages_word_count_total is None or self.content_pages == 0:
            return None

        return self.content_pages_word_count_total / self.content_pages

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
            content_pages_word_count_total=model.words_in_content_pages,
        )


@strawberry.type
class WikibaseStatisticsUsersObservationStrawberryModel:
    """Wikibase Statistics User Data"""

    total_users: Optional[int] = strawberry.field(
        description="Total Users", graphql_type=Optional[BigInt]
    )
    active_users: Optional[int] = strawberry.field(
        description="Active Users", graphql_type=Optional[BigInt]
    )
    total_admin: Optional[int] = strawberry.field(
        description="Total Admin", graphql_type=Optional[BigInt]
    )

    @classmethod
    def marshal(
        cls, model: WikibaseStatisticsObservationModel
    ) -> "WikibaseStatisticsUsersObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if (
            model.total_users is None
            or model.active_users is None
            or model.total_admin is None
        ):
            raise ValueError(
                f"Statistics Observation {model.id}: Expected totals when observation returned data"
            )
        return cls(
            total_users=model.total_users,
            active_users=model.active_users,
            total_admin=model.total_admin,
        )


@strawberry.type
class WikibaseStatisticsObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase Statistics Data Observation"""

    edits: Optional[WikibaseStatisticsEditsObservationStrawberryModel]
    files: Optional[WikibaseStatisticsFilesObservationStrawberryModel]
    pages: Optional[WikibaseStatisticsPagesObservationStrawberryModel]
    users: Optional[WikibaseStatisticsUsersObservationStrawberryModel]

    @classmethod
    def marshal(
        cls, model: WikibaseStatisticsObservationModel
    ) -> "WikibaseStatisticsPagesObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            edits=(
                WikibaseStatisticsEditsObservationStrawberryModel.marshal(model)
                if model.returned_data
                else None
            ),
            files=(
                WikibaseStatisticsFilesObservationStrawberryModel.marshal(model)
                if model.returned_data
                else None
            ),
            pages=(
                WikibaseStatisticsPagesObservationStrawberryModel.marshal(model)
                if model.returned_data
                else None
            ),
            users=(
                WikibaseStatisticsUsersObservationStrawberryModel.marshal(model)
                if model.returned_data
                else None
            ),
        )
