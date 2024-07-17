"""Observations"""

from model.database.wikibase_observation.connectivity import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
    WikibaseConnectivityObservationModel,
)
from model.database.wikibase_observation.log import (
    WikibaseLogMonthObservationModel,
    WikibaseLogMonthTypeObservationModel,
    WikibaseLogMonthUserObservationModel,
    WikibaseLogObservationModel,
)
from model.database.wikibase_observation.property import (
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
from model.database.wikibase_observation.version import (
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)
