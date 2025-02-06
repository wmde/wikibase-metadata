"""Wikibase Language Set Strawberry Model"""

from typing import Optional
import strawberry

from model.database import WikibaseModel


@strawberry.type
class WikibaseLanguageSetStrawberryModel:
    """Wikibase Language Set"""

    primary: Optional[str] = strawberry.field(description="Primary Language")
    additional: list[str] = strawberry.field(description="Additional Languages")

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseLanguageSetStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            primary=(
                model.primary_language.language
                if model.primary_language is not None
                else None
            ),
            additional=[l.language for l in model.additional_languages],
        )
