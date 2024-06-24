"""GraphQL Query"""

from typing import List
import strawberry

from model.strawberry.output import WikibaseStrawberryModel
from resolvers import get_wikibase, get_wikibase_list


@strawberry.type
class Query:
    """GraphQL Query"""

    wikibase: WikibaseStrawberryModel = strawberry.field(
        description="Wikibase Instance", resolver=get_wikibase
    )
    wikibase_list: List[WikibaseStrawberryModel] = strawberry.field(
        description="List of Wikibases", resolver=get_wikibase_list
    )
