"""Database Models"""

from model.database.base import ModelBase
from model.database.wikibase_category_model import WikibaseCategoryModel
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
    WikibaseConnectivityObservationModel,
    WikibaseLogMonthLogTypeObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseLogMonthUserTypeObservationModel,
    WikibaseLogObservationModel,
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseUserGroupModel,
    WikibaseUserObservationGroupModel,
    WikibaseUserObservationModel,
)
from model.database.wikibase_url_model import WikibaseURLModel
