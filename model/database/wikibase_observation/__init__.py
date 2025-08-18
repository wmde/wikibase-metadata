"""Observation Tables"""

from model.database.wikibase_observation.connectivity import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
    WikibaseConnectivityObservationModel,
)
from model.database.wikibase_observation.log import (
    WikibaseLogMonthLogTypeObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseLogMonthUserTypeObservationModel,
)
from model.database.wikibase_observation.property import (
    WikibasePropertyPopularityObservationModel,
    WikibasePropertyPopularityCountModel,
)
from model.database.wikibase_observation.quantity import (
    WikibaseQuantityObservationModel,
)
from model.database.wikibase_observation.recent_changes import (
    WikibaseRecentChangesObservationModel,
)
from model.database.wikibase_observation.statistics import (
    WikibaseStatisticsObservationModel,
)
from model.database.wikibase_observation.time_to_first_value import (
    WikibaseTimeToFirstValueObservationModel,
    WikibaseItemDateModel,
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
