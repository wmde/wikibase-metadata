"""Wikibase Observation Models"""

from model.strawberry.output.observation.connectivity import (
    WikibaseConnectivityObservationStrawberryModel,
)
from model.strawberry.output.observation.log import (
    WikibaseLogObservationStrawberryModel,
    WikibaseYearCreatedAggregated,
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
from model.strawberry.output.observation.software_version import (
    WikibaseSoftwareVersionAggregateStrawberryModel,
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel,
    WikibaseSoftwareVersionObservationStrawberryModel,
    WikibaseSoftwareVersionStrawberryModel,
)
from model.strawberry.output.observation.statistics import (
    WikibaseStatisticsObservationStrawberryModel,
)
from model.strawberry.output.observation.user import (
    WikibaseUserAggregate,
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
