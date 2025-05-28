"""Wikibase Connectivity Data Observation Strawberry Model"""

from datetime import datetime
from typing import Optional
import strawberry

from model.database import WikibaseInitialValueObservationModel
from model.strawberry.output.observation.initial_value.item_date import (
    WikibaseItemDateStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)


@strawberry.type(name="WikibaseInitialValueObservation")
class WikibaseInitialValueObservationStrawberryModel(
    WikibaseObservationStrawberryModel
):
    """Wikibase Initial Value Data Observation"""

    initiation_date: Optional[datetime] = strawberry.field(
        description="Wikibase Initiation Date"
    )

    item_dates: list[WikibaseItemDateStrawberryModel] = strawberry.field(
        description="Item Creation Date"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseInitialValueObservationModel
    ) -> "WikibaseInitialValueObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            initiation_date=model.initiation_date,
            item_dates=[
                WikibaseItemDateStrawberryModel.marshal(o)
                for o in model.item_date_models
            ],
        )
