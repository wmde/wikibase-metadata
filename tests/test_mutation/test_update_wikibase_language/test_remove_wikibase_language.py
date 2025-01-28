"""Test Remove Wikibase Language"""

import pytest

from tests.test_schema import test_schema
from tests.utils.assert_property_value import assert_layered_property_value

WIKIBASE_LANGUAGES_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    languages {
      primary
      additional
    }
  }
}"""

REMOVE_WIKIBASE_LANGUAGE_QUERY = """
mutation MyMutation($language: String!, $wikibaseId: Int!) {
  removeWikibaseLanguage(language: $language, wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="remove-wikibase-language-1",
    depends=["add-wikibase-language-1"],
    scope="session",
)
async def test_remove_wikibase_language_one():
    """Add Wikibase Language"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None
    assert_layered_property_value(
        before_removing_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )

    remove_result = await test_schema.execute(
        REMOVE_WIKIBASE_LANGUAGE_QUERY,
        variable_values={"wikibaseId": 1, "language": "French"},
    )
    assert remove_result.errors is not None
    assert (
        remove_result.errors[0].message
        == "Cannot Remove Primary Language; Please Update First"
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="remove-wikibase-language-2",
    depends=["add-wikibase-language-2"],
    scope="session",
)
async def test_remove_wikibase_language_two():
    """Add Wikibase Language"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None
    assert_layered_property_value(
        before_removing_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch", "English"],
    )

    remove_result = await test_schema.execute(
        REMOVE_WIKIBASE_LANGUAGE_QUERY,
        variable_values={"wikibaseId": 1, "language": "English"},
    )
    assert remove_result.errors is None
    assert remove_result.data is not None
    assert remove_result.data["removeWikibaseLanguage"] is True

    after_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
    )
    assert after_removing_result.errors is None
    assert after_removing_result.data is not None
    assert_layered_property_value(
        after_removing_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch"],
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="remove-wikibase-language-3",
    depends=["remove-wikibase-language-2"],
    scope="session",
)
async def test_remove_wikibase_language_three():
    """Add Wikibase Language"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None
    assert_layered_property_value(
        before_removing_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch"],
    )

    remove_result = await test_schema.execute(
        REMOVE_WIKIBASE_LANGUAGE_QUERY,
        variable_values={"wikibaseId": 1, "language": "Greek"},
    )
    assert remove_result.errors is None
    assert remove_result.data is not None
    assert remove_result.data["removeWikibaseLanguage"] is True

    after_removing_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
    )
    assert after_removing_result.errors is None
    assert after_removing_result.data is not None
    assert_layered_property_value(
        after_removing_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Albanian", "Babylonian", "Cymru", "Deutsch"],
    )
