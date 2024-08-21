"""Wikibase Statistics Data Observation Strawberry Models"""

from typing import Optional
import strawberry

from model.database import WikibaseStatisticsObservationModel
from model.strawberry.output.observation.statistics.component import (
    WikibaseStatisticsEditsObservationStrawberryModel,
    WikibaseStatisticsFilesObservationStrawberryModel,
    WikibaseStatisticsPagesObservationStrawberryModel,
    WikibaseStatisticsUsersObservationStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
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
