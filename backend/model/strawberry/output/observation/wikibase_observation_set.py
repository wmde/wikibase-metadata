"""Wikibase Observation Set Strawberry Model"""

from typing import Generic, Optional, TypeVar
import strawberry

from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)


T = TypeVar("T", bound=WikibaseObservationStrawberryModel)


@strawberry.type(name="WikibaseObservationSet")
class WikibaseObservationSetStrawberryModel(Generic[T]):
    """Wikibase Observation Set"""

    all_observations: list[T] = strawberry.field(description="All Observations")

    @strawberry.field(description="Most Recent Observation that Returned Data")
    def most_recent(self) -> Optional[T]:
        """Most Recent Observation that Returned Data"""

        successful_observations = [
            datum for datum in self.all_observations if datum.returned_data
        ]
        if len(successful_observations) > 0:
            return max(successful_observations, key=lambda x: x.observation_date)
        return None

    @classmethod
    def marshal(cls, data: list[T]):
        """Coerce List into Set"""

        return cls(all_observations=data)
