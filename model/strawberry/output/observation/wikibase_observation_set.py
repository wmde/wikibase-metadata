"""Wikibase User Data Observation Set Strawberry Model"""

from typing import Generic, List, Optional, TypeVar
import strawberry

from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)


T = TypeVar("T", bound=WikibaseObservationStrawberryModel)


@strawberry.type
class WikibaseObservationSetStrawberryModel(Generic[T]):
    """Wikibase Data Observation Set"""

    all_observations: List[T] = strawberry.field(description="All Observations")
    most_recent: Optional[T] = strawberry.field(
        description="Most Recent Observation that Returned Data"
    )

    @classmethod
    def marshal(cls, data: List[T]):
        """Find most recent in list"""

        successful_observations = [datum for datum in data if datum.returned_data]
        return cls(
            all_observations=data,
            most_recent=(
                max(successful_observations, key=lambda x: x.observation_date)
                if len(successful_observations) > 0
                else None
            ),
        )
