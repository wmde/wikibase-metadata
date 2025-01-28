"""Test Update Wikibase Language"""

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
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
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
    )
    assert add_result.errors is None
    assert add_result.data is not None
    assert add_result.data["addWikibaseLanguage"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
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
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "languages", "primary"],
        expected_value='French',
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=[],
    )

    for lang in ['Deutsch', 'Cymru', 'French', 'Albanian', 'English', 'Babylonian']:
        add_result = await test_schema.execute(
            ADD_WIKIBASE_LANGUAGE_QUERY,
            variable_values={"wikibaseId": 1, "language": lang},
        )
        assert add_result.errors is None
        assert add_result.data is not None
        assert add_result.data["addWikibaseLanguage"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": 1}
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
        expected_value=['Albanian', 'Babylonian', 'Cymru', 'Deutsch', 'English'],
    )
