"""Wikibase Instance Strawberry Model"""

from typing import Optional
import strawberry

from model.database import WikibaseModel


@strawberry.type
class WikibaseURLSetStrawberryModel:
    """Wikibase Instance"""

    base_url: str = strawberry.field(description="Base URL")
    action_api: Optional[str] = strawberry.field(description="Action API URL")
    index_api: Optional[str] = strawberry.field(description="Index API URL")
    sparql_url: Optional[str] = strawberry.field(description="SPARQL URL")
    sparql_endpoint_url: Optional[str] = strawberry.field(
        description="SPARQL Endpoint URL"
    )

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseURLSetStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            base_url=model.url,
            action_api=model.action_query_url,
            index_api=model.index_query_url,
            sparql_url=model.sparql_query_url,
            sparql_endpoint_url=model.sparql_endpoint_url,
        )
