"""Wikibase Log Data Observation Strawberry Model"""

import strawberry

from model.database import WikibaseModel
from model.strawberry.output.observation.log.wikibase_log_month_observation import (
    WikibaseLogMonthStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation_set import (
    WikibaseObservationSetStrawberryModel,
)


@strawberry.type(name="WikibaseLogObservation")
class WikibaseLogObservationStrawberryModel:
    """Wikibase Log Data Observation"""

    first_month: WikibaseObservationSetStrawberryModel[
        WikibaseLogMonthStrawberryModel
    ] = strawberry.field(description="First Month's Logs")
    last_month: WikibaseObservationSetStrawberryModel[
        WikibaseLogMonthStrawberryModel
    ] = strawberry.field(description="Last Month's Logs")

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseLogObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            first_month=(
                WikibaseObservationSetStrawberryModel.marshal(
                    [
                        WikibaseLogMonthStrawberryModel.marshal(m)
                        for m in model.log_month_observations
                        if m.first_month
                    ]
                )
            ),
            last_month=(
                WikibaseObservationSetStrawberryModel.marshal(
                    [
                        WikibaseLogMonthStrawberryModel.marshal(m)
                        for m in model.log_month_observations
                        if not m.first_month
                    ]
                )
            ),
        )
