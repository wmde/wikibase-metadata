"""Merge Software"""

from data.database_connection import get_async_session
from fetch_data.utils import get_wikibase_from_database
from model.database import WikibaseLanguageModel, WikibaseModel


async def add_wikibase_language(wikibase_id: int, language: str) -> bool:
    """
    Add Additional Language to Wikibase

    Will return `True` if language present in Wikibase's list -
    regardless of whether previously existing or newly inserted
    """

    clean_language = clean_up_language(language)

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )
        if clean_language not in [l.language for l in wikibase.languages]:
            wikibase.languages.append(
                WikibaseLanguageModel(
                    language=clean_language, primary=(len(wikibase.languages) == 0)
                )
            )
        await async_session.commit()

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )
        return clean_language in [l.language for l in wikibase.languages]


async def remove_wikibase_language(wikibase_id: int, language: str) -> bool:
    """
    Remove Language from Wikibase

    Will return `True` if language absent in Wikibase's list -
    regardless of whether never present or newly removed
    """

    clean_language = clean_up_language(language)

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )

        if (
            wikibase.primary_language is not None
            and wikibase.primary_language.language == clean_language
        ):
            raise ValueError("Cannot Remove Primary Language; Please Update First")

        found = False
        for l in wikibase.additional_languages:
            if (not found) and l.language == clean_language:
                found = True
                wikibase.languages.remove(l)

        await async_session.commit()

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )
        return clean_language not in [l.language for l in wikibase.languages]


async def update_wikibase_primary_language(wikibase_id: int, language: str) -> bool:
    """
    Update Wikibase Language

    Will add language if not already in `additional` list

    Will move previous primary language to `additional` list

    Will return `True` if language is Wikibase's primary -
    regardless of whether previously recorded or newly updated
    """

    clean_language = clean_up_language(language)

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )
        if (
            wikibase.primary_language is None
            or wikibase.primary_language.language != clean_language
        ):
            if wikibase.primary_language is not None:
                wikibase.primary_language.primary = False

            found = False
            for l in wikibase.additional_languages:
                if (not found) and l.language == clean_language:
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


def clean_up_language(language: str) -> str:
    """Clean Language Name"""

    return language.strip()
