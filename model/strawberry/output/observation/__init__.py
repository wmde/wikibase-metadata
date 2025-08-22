"""Wikibase Observation Models"""

from model.strawberry.output.observation.connectivity import (
    WikibaseConnectivityObservationStrawberryModel,
)
from model.strawberry.output.observation.log import (
    WikibaseLogObservationStrawberryModel,
    WikibaseYearCreatedAggregateStrawberryModel,
)
from model.strawberry.output.observation.property_popularity import (
    WikibasePropertyPopularityAggregateCountStrawberryModel,
    WikibasePropertyPopularityCountStrawberryModel,
    WikibasePropertyPopularityObservationStrawberryModel,
)
from model.strawberry.output.observation.quantity import (
    WikibaseQuantityAggregateStrawberryModel,
    WikibaseQuantityObservationStrawberryModel,
)
from model.strawberry.output.observation.external_identifier import (
    WikibaseExternalIdentifierAggregateStrawberryModel,
    WikibaseExternalIdentifierObservationStrawberryModel,
)
from model.strawberry.output.observation.url import (
    WikibaseURLAggregateStrawberryModel,
    WikibaseURLObservationStrawberryModel,
)
from model.strawberry.output.observation.recent_changes import (
    WikibaseRecentChangesAggregateStrawberryModel,
    WikibaseRecentChangesObservationStrawberryModel,
)
from model.strawberry.output.observation.software_version import (
    WikibaseSoftwareVersionAggregateStrawberryModel,
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel,
    WikibaseSoftwareVersionObservationStrawberryModel,
    WikibaseSoftwareVersionStrawberryModel,
)
from model.strawberry.output.observation.statistics import (
    WikibaseStatisticsAggregateStrawberryModel,
    WikibaseStatisticsObservationStrawberryModel,
)
from model.strawberry.output.observation.user import (
    WikibaseUserAggregateStrawberryModel,
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
