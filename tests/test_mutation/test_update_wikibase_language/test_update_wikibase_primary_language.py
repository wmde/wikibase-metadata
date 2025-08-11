"""Test Update Primary Language"""

import pytest

from tests.test_schema import test_schema
from tests.test_mutation.test_update_wikibase_language.query import (
    WIKIBASE_LANGUAGES_QUERY,
)
from tests.utils import assert_layered_property_value, get_mock_context
from resolvers import update_wikibase_primary_language

UPDATE_WIKIBASE_PRIMARY_LANGUAGE_QUERY = """
mutation MyMutation($language: String!, $wikibaseId: Int!) {
  updateWikibasePrimaryLanguage(language: $language, wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="update-wikibase-primary-language-1",
    depends=["remove-wikibase-language-2"],
    scope="session",
)
async def test_update_wikibase_primary_language_to_current_additional():
    """
    Test Updating Primary Language

    Primary exists; new Primary already listed in Additional
    """

    before_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch"],
    )

    update_result = await test_schema.execute(
        UPDATE_WIKIBASE_PRIMARY_LANGUAGE_QUERY,
        variable_values={"wikibaseId": 1, "language": "Cymru"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["updateWikibasePrimaryLanguage"] is True

    after_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="Cymru",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Deutsch", "French"],
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="update-wikibase-primary-language-2",
    depends=["update-wikibase-primary-language-1"],
    scope="session",
)
async def test_update_wikibase_primary_language_to_new():
    """
    Test Updating Primary Language

    Primary exists; new Primary not listed in Additional
    """

    before_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="Cymru",
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Deutsch", "French"],
    )

    update_result = await update_wikibase_primary_language(1, "Hindi")
    assert update_result

    after_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="Hindi",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch", "French"],
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="update-wikibase-primary-language-3",
    depends=["update-wikibase-primary-language-2"],
    scope="session",
)
async def test_update_wikibase_primary_language_to_same():
    """
    Test Updating Primary Language

    Primary exists; new Primary same as Primary
    """

    before_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="Hindi",
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch", "French"],
    )

    update_result = await update_wikibase_primary_language(1, "Hindi")
    assert update_result

    after_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="Hindi",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch", "French"],
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="update-wikibase-primary-language-4",
    depends=["mutate-cloud-instances"],
    scope="session",
)
async def test_update_wikibase_new_primary_language():
    """
    Test Updating Primary Language

    Primary does not exist
    """

    before_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 5},
        context_value=get_mock_context("test-auth-token"),
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value="5"
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value=None,
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=[],
    )

    update_result = await update_wikibase_primary_language(5, "Íslenska")
    assert update_result

    after_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY,
        variable_values={"wikibaseId": 5},
        context_value=get_mock_context("test-auth-token"),
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value="5"
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="Íslenska",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=[],
    )
