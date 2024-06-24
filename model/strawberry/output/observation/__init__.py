"""Wikibase Observation Models"""

from model.strawberry.output.observation.connectivity import (
    WikibaseConnectivityObservationStrawberryModel,
)
from model.strawberry.output.observation.quantity import (
    WikibaseQuantityObservationStrawberryModel,
)
from model.strawberry.output.observation.user import (
    WikibaseUserGroupStrawberryModel,
    WikibaseUserObservationStrawberryModel,
    WikibaseUserObservationGroupStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation_set import (
    WikibaseObservationSetStrawberryModel,
)
