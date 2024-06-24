"""Wikibase Connectivity Observation Item / Relationship Count Strawberry Model"""

import strawberry

from model.database import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
)


@strawberry.type
class WikibaseConnectivityObservationRelationshipCountStrawberryModel:
    """Wikibase Connectivity Observation Relationship Counts"""

    id: strawberry.ID
    relationship_count: int = strawberry.field(
        description="Number of Relationships Defined for Item"
    )


@strawberry.type
class WikibaseConnectivityObservationItemRelationshipCountStrawberryModel(
    WikibaseConnectivityObservationRelationshipCountStrawberryModel
):
    """Wikibase Connectivity Observation Item / Relationship Counts"""

    item_count: int = strawberry.field(
        description="Number of Items with This Relationship Count"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseConnectivityObservationItemRelationshipCountModel
    ) -> "WikibaseConnectivityObservationItemRelationshipCountStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            relationship_count=model.relationship_count,
            item_count=model.item_count,
        )


@strawberry.type
class WikibaseConnectivityObservationObjectRelationshipCountStrawberryModel(
    WikibaseConnectivityObservationRelationshipCountStrawberryModel
):
    """Wikibase Connectivity Observation Object / Relationship Counts"""

    object_count: int = strawberry.field(
        description="Number of Object with This Relationship Count"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseConnectivityObservationObjectRelationshipCountModel
    ) -> "WikibaseConnectivityObservationObjectRelationshipCountStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            relationship_count=model.relationship_count,
            object_count=model.object_count,
        )
