# pylint: disable=redefined-outer-name
"""Test Update Primary Language"""

import pytest
import pytest_asyncio

from tests.test_schema import test_schema
from tests.test_mutation.test_update_wikibase_language.query import (
    WIKIBASE_LANGUAGES_QUERY,
)
from tests.utils import assert_layered_property_value, get_mock_context
from resolvers import update_wikibase_primary_language, add_wikibase_language
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel

UPDATE_WIKIBASE_PRIMARY_LANGUAGE_MUTATION = """
mutation MyMutation($language: String!, $wikibaseId: Int!) {
  updateWikibasePrimaryLanguage(language: $language, wikibaseId: $wikibaseId)
}"""


@pytest_asyncio.fixture(scope="function")
async def get_wikibase_without_primary_language():
    """Get the ID of a wikibase that has no primary language"""
    list_result = await test_schema.execute("""
        query {
          wikibaseList(pageNumber: 1, pageSize: 100) {
            data {
              id
              languages {
                primary
              }
            }
          }
        }
        """)
    assert list_result.errors is None
    assert list_result.data is not None

    # Find first wikibase without primary language
    for wikibase in list_result.data["wikibaseList"]["data"]:
        if wikibase["languages"]["primary"] is None:
            return int(wikibase["id"])

    pytest.fail("No wikibase found without primary language")

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
@pytest.mark.dependency(
    name="update-wikibase-primary-language-1",
    scope="session",
)
async def test_update_wikibase_primary_language_to_current_additional(
    wikibase_with_additional_languages,
):
    """
    Test Updating Primary Language

    Primary exists; new Primary already listed in Additional
    """

    wikibase_id = wikibase_with_additional_languages.id

    before_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Cymru", "Deutsch"],
    )

    update_result = await test_schema.execute(
        UPDATE_WIKIBASE_PRIMARY_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": wikibase_id, "language": "Cymru"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["updateWikibasePrimaryLanguage"] is True

    after_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="Cymru",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Deutsch", "French"],
    )


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="update-wikibase-primary-language-2",
    scope="session",
)
async def test_update_wikibase_primary_language_to_new(wikibase_with_additional_languages):
    """
    Test Updating Primary Language

    Primary exists; new Primary not listed in Additional
    """

    wikibase_id = wikibase_with_additional_languages.id

    before_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Cymru", "Deutsch"],
    )

    update_result = await update_wikibase_primary_language(wikibase_id, "Hindi")
    assert update_result

    after_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="Hindi",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Cymru", "Deutsch", "French"],
    )


@pytest.mark.asyncio
async def test_update_wikibase_primary_language_to_same(wikibase_with_additional_languages):
    """
    Test Updating Primary Language

    Primary exists; new Primary same as Primary
    """

    wikibase_id = wikibase_with_additional_languages.id
    before_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Cymru", "Deutsch"],
    )

    update_result = await update_wikibase_primary_language(wikibase_id, "French")
    assert update_result

    after_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "primary"],
        expected_value="French",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "languages", "additional"],
        expected_value=["Cymru", "Deutsch"],
    )

@pytest.fixture
async def wikibase_without_language(db_session):  # pylint: disable=unused-argument
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


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_update_wikibase_new_primary_language(
    wikibase_without_language,
):
    """
    Test Updating Primary Language

    Primary does not exist
    """

    wikibase_id = wikibase_without_language.id

    before_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
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

    update_result = await update_wikibase_primary_language(wikibase_id, "Íslenska")
    assert update_result

    after_updating_result = await test_schema.execute(
        WIKIBASE_LANGUAGES_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
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
