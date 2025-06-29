"""Test Data Expectations with Great Expectations"""

import pytest
from model.database import WikibaseModel, WikibaseLanguageModel, WikibaseURLModel
from sqlalchemy import select
from data import get_async_session


def test_setting_two_primary_languages():
    """
    test whether setting different primary languages
    marks the former one non primary
    """

    wikibase = WikibaseModel(
        wikibase_name="Some Wikibase",
        base_url="https://wikibase.example",
    )
    wikibase.set_primary_language("ko")
    wikibase.set_primary_language("ja")

    primary_languages = list(filter(lambda l: l.primary, wikibase.languages))
    assert len(primary_languages) == 1
    assert primary_languages[0].language == "ja"
    assert len(wikibase.languages) == 2


@pytest.mark.asyncio
async def test_setting_existing_language_as_primary():
    """
    test whether setting a primary language that exists
    as non primary already does not add additional language items
    """

    async with get_async_session() as async_session:
        wikibase = WikibaseModel(
            wikibase_name="Some Wikibase",
            base_url="https://unique.wikibase.example",
        )
        async_session.add(wikibase)

        wikibase.languages.append(WikibaseLanguageModel("ko"))

        assert len(wikibase.languages) == 1
        assert wikibase.primary_language is None

        wikibase.set_primary_language("ko")

        await async_session.flush()

        stmt = (
            select(WikibaseModel)
            .join(WikibaseModel.url)
            .where(WikibaseURLModel.url == "https://unique.wikibase.example")
        )
        found = (await async_session.scalars(stmt)).one_or_none()

        assert found is not None
        assert len(found.languages) == 1
        assert found.primary_language.language == "ko"


def test_setting_two_identical_languages():
    """
    test setting additional languages multiple times
    does not add identical languages
    """

    wikibase = WikibaseModel(
        wikibase_name="Some Wikibase",
        base_url="https://wikibase.example",
        additional_languages=["ko"],
    )
    wikibase.set_additional_languages(["ko"])
    assert len(wikibase.languages) == 1
    wikibase.set_additional_languages(["ko", "ja"])
    assert len(wikibase.languages) == 2
    wikibase.set_additional_languages(["ko", "ja"])
    assert len(wikibase.languages) == 2


@pytest.mark.asyncio
async def test_setting_primary_language_again_does_not_do_anything():
    """
    the existing primary language object should be reused
    if this language is already set as primary
    """

    async with get_async_session() as async_session:
        wikibase = WikibaseModel(
            wikibase_name="Some Wikibase",
            base_url="https://unique.wikibase.example",
            primary_language="ko",
        )
        async_session.add(wikibase)
        await async_session.flush()
        await async_session.refresh(wikibase)
        old_language = wikibase.primary_language

        wikibase.set_primary_language("ko")
        assert wikibase.primary_language is old_language


@pytest.mark.asyncio
async def test_update_existing_article_path():
    """
    update article_path when it is already set
    """

    async with get_async_session() as async_session:
        wikibase = WikibaseModel(
            wikibase_name="Some Wikibase",
            base_url="https://unique.wikibase.example",
            article_path="w",
        )
        async_session.add(wikibase)
        await async_session.flush()
        await async_session.refresh(wikibase)

        assert wikibase.article_path.url == "w"

        wikibase.set_article_path("wiki-article")
        await async_session.flush()
        await async_session.refresh(wikibase)

        assert wikibase.article_path.url == "wiki-article"


@pytest.mark.asyncio
async def test_update_existing_script_path():
    """
    update script_path when it is already set
    """

    async with get_async_session() as async_session:
        wikibase = WikibaseModel(
            wikibase_name="Some Wikibase",
            base_url="https://unique.wikibase.example",
            script_path="w",
        )
        async_session.add(wikibase)
        await async_session.flush()
        await async_session.refresh(wikibase)

        assert wikibase.script_path.url == "w"

        wikibase.set_script_path("wiki-script")
        await async_session.flush()
        await async_session.refresh(wikibase)

        assert wikibase.script_path.url == "wiki-script"


@pytest.mark.asyncio
async def test_update_existing_sparql_endpoint():
    """
    update sparql_endpoint when it is already set
    """

    async with get_async_session() as async_session:
        wikibase = WikibaseModel(
            wikibase_name="Some Wikibase",
            base_url="https://unique.wikibase.example",
            sparql_endpoint_url="https://unique.wikibase.example/wrong-sparql/sparql",
        )
        async_session.add(wikibase)
        await async_session.flush()
        await async_session.refresh(wikibase)

        assert (
            wikibase.sparql_endpoint_url.url
            == "https://unique.wikibase.example/wrong-sparql/sparql"
        )

        wikibase.set_sparql_endpoint_url(
            "https://unique.wikibase.example/sparql/sparql"
        )
        await async_session.flush()
        await async_session.refresh(wikibase)

        assert (
            wikibase.sparql_endpoint_url.url
            == "https://unique.wikibase.example/sparql/sparql"
        )


@pytest.mark.asyncio
async def test_update_existing_sparql_frontend():
    """
    update sparql_frontend when it is already set
    """

    async with get_async_session() as async_session:
        wikibase = WikibaseModel(
            wikibase_name="Some Wikibase",
            base_url="https://unique.wikibase.example",
            sparql_frontend_url="https://unique.wikibase.example/wrong-sparql",
        )
        async_session.add(wikibase)
        await async_session.flush()
        await async_session.refresh(wikibase)

        assert (
            wikibase.sparql_frontend_url.url
            == "https://unique.wikibase.example/wrong-sparql"
        )

        wikibase.set_sparql_frontend_url("https://unique.wikibase.example/sparql")
        await async_session.flush()
        await async_session.refresh(wikibase)

        assert (
            wikibase.sparql_frontend_url.url == "https://unique.wikibase.example/sparql"
        )
