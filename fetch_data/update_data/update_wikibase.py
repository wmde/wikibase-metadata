"""Merge Software"""

from data.database_connection import get_async_session
from fetch_data.utils import get_wikibase_from_database
from model.database import WikibaseLanguageModel, WikibaseModel


async def update_wikibase_primary_language(wikibase_id: int, language: str) -> bool:
    """Update Wikibase Language"""

    clean_language = language.strip()

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )
        if (
            wikibase.primary_language is None
            or wikibase.primary_language.language != clean_language
        ):
            found = False
            for l in wikibase.additional_languages:
                if (not found) and l.language == clean_language:
                    if wikibase.primary_language is not None:
                        wikibase.languages.remove(wikibase.primary_language)
                    l.primary = True
                    found = True

            if not found:
                wikibase.languages.append(
                    WikibaseLanguageModel(language=clean_language, primary=True)
                )
        await async_session.commit()

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )
        return wikibase.primary_language.language == clean_language
