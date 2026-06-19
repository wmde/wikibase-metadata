"""Test Update Wikibase Language"""

import pytest

from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from tests.test_mutation.test_update_wikibase_language.query import (
    WIKIBASE_LANGUAGES_QUERY,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context
from resolvers import add_wikibase_language

ADD_WIKIBASE_LANGUAGE_MUTATION = """
mutation MyMutation($language: String!, $wikibaseId: Int!) {
  addWikibaseLanguage(language: $language, wikibaseId: $wikibaseId)
}"""

@pytest.fixture
async def wikibase_without_primary_language(db_session):  # pylint: disable=unused-argument
    """Create a test wikibase"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://wikibase-fixture.com",
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()

        return wikibase

@pytest.fixture
async def wikibase_without_additional_languages(db_session):  # pylint: disable=unused-argument
    """Create a test wikibase"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://wikibase-fixture.com",
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()

        await add_wikibase_language(wikibase.id, "French")
        return wikibase


@pytest.mark.asyncio
async def test_add_wikibase_language_one(wikibase_without_primary_language):
    """Add Wikibase Language"""

    wikibase_id = wikibase_without_primary_language.id

    before_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "languages", "primary"],
        expected_value=None,
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=[],
    )

    add_result = await test_schema.execute(
        ADD_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": wikibase_id, "language": "French"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert add_result.errors is None
    assert add_result.data is not None
    assert add_result.data["addWikibaseLanguage"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=[],
    )


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_add_wikibase_language_two(wikibase_without_additional_languages):
    """Add Wikibase Language"""

    wikibase_id = wikibase_without_additional_languages.id

    before_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=[],
    )

    for lang in ["Deutsch", "Cymru", "French", "Albanian", "English", "Babylonian"]:
        add_result = await add_wikibase_language(wikibase_id=wikibase_id, language=lang)
        assert add_result

    after_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch", "English"],
    )
