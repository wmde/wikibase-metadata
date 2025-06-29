"""Test Update Wikibase Language"""

import pytest

from tests.test_mutation.test_update_wikibase_language.query import (
    WIKIBASE_LANGUAGES_QUERY,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context
from update_data import add_wikibase_language


ADD_WIKIBASE_LANGUAGE_QUERY = """
mutation MyMutation($language: String!, $wikibaseId: Int!) {
  addWikibaseLanguage(language: $language, wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="add-wikibase-language-1", depends=["add-wikibase"], scope="session"
)
async def test_add_wikibase_language_one():
    """Add Wikibase Language"""

    before_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value="1"
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
        ADD_WIKIBASE_LANGUAGE_QUERY,
        variable_values={"wikibaseId": 1, "language": "French"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert add_result.errors is None
    assert add_result.data is not None
    assert add_result.data["addWikibaseLanguage"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["wikibase", "id"], expected_value="1"
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
@pytest.mark.dependency(
    name="add-wikibase-language-2", depends=["add-wikibase-language-1"], scope="session"
)
async def test_add_wikibase_language_two():
    """Add Wikibase Language"""

    before_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value="1"
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
        add_result = await add_wikibase_language(wikibase_id=1, language=lang)
        assert add_result

    after_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["wikibase", "id"], expected_value="1"
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
