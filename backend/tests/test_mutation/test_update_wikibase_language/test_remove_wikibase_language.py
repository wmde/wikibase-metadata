"""Test Remove Wikibase Language"""

import pytest

from tests.test_mutation.test_update_wikibase_language.query import (
    WIKIBASE_LANGUAGES_QUERY,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context
from resolvers import remove_wikibase_language
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from resolvers import add_wikibase_language
REMOVE_WIKIBASE_LANGUAGE_MUTATION = """
mutation MyMutation($language: String!, $wikibaseId: Int!) {
  removeWikibaseLanguage(language: $language, wikibaseId: $wikibaseId)
}"""

@pytest.fixture
async def wikibase(db_session):  # pylint: disable=unused-argument
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

@pytest.fixture
async def wikibase_with_additional_languages(db_session):  # pylint: disable=unused-argument
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

        for lang in ["Deutsch", "Cymru"]:
            await add_wikibase_language(wikibase_id=wikibase.id, language=lang)
        return wikibase

@pytest.mark.asyncio
@pytest.mark.mutation
async def test_remove_wikibase_language_one(wikibase):
    """Remove Wikibase Language - Primary"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None
    assert_layered_property_value(
        before_removing_result.data, ["wikibase", "id"], expected_value=str(wikibase.id)
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )

    remove_result = await test_schema.execute(
        REMOVE_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": wikibase.id, "language": "French"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert remove_result.errors is not None
    assert (
        remove_result.errors[0].message
        == "Cannot Remove Primary Language; Please Update First"
    )


@pytest.mark.asyncio
async def test_remove_wikibase_language_two(wikibase_with_additional_languages):
    """Remove Wikibase Language - Additional"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_with_additional_languages.id}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None
    assert_layered_property_value(
        before_removing_result.data, ["wikibase", "id"], expected_value=str(wikibase_with_additional_languages.id)
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Cymru", "Deutsch"],
    )

    remove_result = await remove_wikibase_language(wikibase_id=wikibase_with_additional_languages.id, language="Cymru")
    assert remove_result

    after_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_with_additional_languages.id}
    )
    assert after_removing_result.errors is None
    assert after_removing_result.data is not None
    assert_layered_property_value(
        after_removing_result.data, ["wikibase", "id"], expected_value=str(wikibase_with_additional_languages.id)
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Deutsch"],
    )


@pytest.mark.asyncio
async def test_remove_wikibase_language_three(wikibase_with_additional_languages):
    """Remove Wikibase Language - Does Not Exist in List"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_with_additional_languages.id}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Cymru", "Deutsch"],
    )

    remove_result = await remove_wikibase_language(wikibase_id=wikibase_with_additional_languages.id, language="Greek")
    assert remove_result

    after_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_with_additional_languages.id}
    )
    assert after_removing_result.errors is None
    assert after_removing_result.data is not None
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Cymru", "Deutsch"],
    )