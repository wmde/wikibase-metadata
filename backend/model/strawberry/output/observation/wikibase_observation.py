"""Wikibase Observation Strawberry Model"""

from datetime import datetime
import strawberry


@strawberry.type(name="WikibaseObservation")
class WikibaseObservationStrawberryModel:
    """Wikibase Data Observation - ABSTRACT"""

    id: strawberry.ID
    observation_date: datetime = strawberry.field(description="Observation Date")
    returned_data: bool = strawberry.field(description="Returned Data?")
