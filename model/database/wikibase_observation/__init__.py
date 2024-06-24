"""Observations"""

from model.database.wikibase_observation.connectivity import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
    WikibaseConnectivityObservationModel,
)
from model.database.wikibase_observation.property_popularity import (
    WikibasePropertyPopularityObservationModel,
    WikibasePropertyPopularityCountModel,
)
from model.database.wikibase_observation.quantity import (
    WikibaseQuantityObservationModel,
)
from model.database.wikibase_observation.user import (
    WikibaseUserGroupModel,
    WikibaseUserObservationGroupModel,
    WikibaseUserObservationModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)
