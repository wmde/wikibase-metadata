"""Wikibase Log Strawberry Models"""

from datetime import datetime
from typing import Optional
import strawberry


@strawberry.type
class WikibaseLogStrawberryModel:
    """Wikibase Log"""

    date: datetime = strawberry.field(description="Log Date")


@strawberry.type
class WikibaseLogUserStrawberryModel(WikibaseLogStrawberryModel):
    """Wikibase Log"""

    user_type: Optional[str] = strawberry.field(
        description="User Type - Bot, User, or Missing?"
    )
