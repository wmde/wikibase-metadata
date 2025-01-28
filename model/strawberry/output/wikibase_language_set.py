"""Wikibase Language Set Strawberry Model"""

import strawberry

from model.database import WikibaseModel


@strawberry.type
class WikibaseLanguageSetStrawberryModel:
    """Wikibase Language Set"""

    primary: str = strawberry.field(description="Primary Language")
    additional: list[str] = strawberry.field(description="Additional Languages")

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseLanguageSetStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            primary=model.primary_language.language,
            additional = [l.language for l in model.additional_languages]
        )
