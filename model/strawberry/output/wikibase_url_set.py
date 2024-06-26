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
    special_version_url: Optional[str] = strawberry.field(
        description="Special:Version URL"
    )

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseURLSetStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            base_url=model.url.url,
            action_api=(
                model.action_api_url.url if model.action_api_url is not None else None
            ),
            index_api=(
                model.index_api_url.url if model.index_api_url is not None else None
            ),
            sparql_url=(
                model.sparql_query_url.url
                if model.sparql_query_url is not None
                else None
            ),
            sparql_endpoint_url=(
                model.sparql_endpoint_url.url
                if model.sparql_endpoint_url is not None
                else None
            ),
            special_version_url=(
                model.special_version_url.url
                if model.special_version_url is not None
                else None
            ),
        )
