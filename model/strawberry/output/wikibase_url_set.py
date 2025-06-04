"""Wikibase URL Set Strawberry Model"""

from typing import Optional
import strawberry

from model.database import WikibaseModel


@strawberry.type(name="WikibaseURLSet")
class WikibaseURLSetStrawberryModel:
    """Wikibase URL Set"""

    base_url: str = strawberry.field(description="Base URL")
    article_path: str = strawberry.field(description="Article Path `/wiki`")
    script_path: str = strawberry.field(description="Script Path `/w`")
    sparql_endpoint_url: Optional[str] = strawberry.field(
        description="SPARQL Endpoint URL"
    )
    sparql_frontend_url: Optional[str] = strawberry.field(
        description="SPARQL Frontend URL"
    )

    action_api: Optional[str] = strawberry.field(
        description="Action API URL", deprecation_reason="Use scriptPath"
    )
    index_api: Optional[str] = strawberry.field(
        description="Index API URL", deprecation_reason="Use scriptPath"
    )
    sparql_url: Optional[str] = strawberry.field(
        description="SPARQL URL",
        deprecation_reason="Renamed to sparqlFrontendURL for clarity",
    )
    special_statistics_url: Optional[str] = strawberry.field(
        description="Special:Statistics URL", deprecation_reason="Use articlePath"
    )
    special_version_url: Optional[str] = strawberry.field(
        description="Special:Version URL", deprecation_reason="Use articlePath"
    )

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseURLSetStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            base_url=model.url.url,
            article_path=model.article_path.url,
            script_path=model.script_path.url,
            sparql_endpoint_url=(
                model.sparql_endpoint_url.url
                if model.sparql_endpoint_url is not None
                else None
            ),
            sparql_frontend_url=(
                model.sparql_frontend_url.url
                if model.sparql_frontend_url is not None
                else None
            ),
            action_api=model.action_api_url(),
            index_api=model.index_api_url(),
            sparql_url=(
                model.sparql_frontend_url.url
                if model.sparql_frontend_url is not None
                else None
            ),
            special_statistics_url=model.special_statistics_url(),
            special_version_url=model.special_version_url(),
        )
