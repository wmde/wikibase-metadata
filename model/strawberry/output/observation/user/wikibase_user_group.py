"""Wikibase User Group Strawberry Model"""

import strawberry

from model.database import WikibaseUserGroupModel


@strawberry.type
class WikibaseUserGroupStrawberryModel:
    """Wikibase User Group"""

    id: strawberry.ID
    group_name: str = strawberry.field(description="Group Name")
    wikibase_default: bool = strawberry.field(description="Wikibase Default Group?")

    @classmethod
    def marshal(
        cls, model: WikibaseUserGroupModel
    ) -> "WikibaseUserGroupStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            group_name=model.group_name,
            wikibase_default=model.wikibase_default_group,
        )
