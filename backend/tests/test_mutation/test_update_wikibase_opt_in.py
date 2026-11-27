# pylint: disable=redefined-outer-name
"""Test Update Wikibase Opt-in Status"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseModel
from tests.test_schema import test_schema
from tests.utils import get_mock_context

UPDATE_WIKIBASE_OPT_IN_MUTATION = """
mutation MyMutation($wikibaseId: Int!, $optIn: Boolean!) {
    updateWikibaseOptIn(wikibaseId: $wikibaseId, optIn: $optIn)
}
"""


@pytest.fixture
async def wikibase(db_session):
    """Create a test Wikibase that has opted in."""
    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://example.com",
            sparql_frontend_url="https://query.example.com",
            sparql_endpoint_url="https://query.example.com/sparql",
            article_path="/wiki",
            opt_in=True,
        )
        session.add(wikibase)
        await session.flush()
        return wikibase


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_update_wikibase_opt_in(wikibase, db_session):
    """Opt out of a Wikibase and then opt back in."""

    # Opt out
    opt_out_result = await test_schema.execute(
        UPDATE_WIKIBASE_OPT_IN_MUTATION,
        variable_values={"wikibaseId": wikibase.id, "optIn": False},
        context_value=get_mock_context("test-auth-token"),
    )

    assert opt_out_result.errors is None
    assert opt_out_result.data is not None
    assert opt_out_result.data["updateWikibaseOptIn"] is True

    async with AsyncSession(bind=db_session) as session:
        updated_wikibase = await session.get(WikibaseModel, wikibase.id)

        assert updated_wikibase.opt_in is False
        assert updated_wikibase.sparql_frontend_url is None
        assert updated_wikibase.sparql_endpoint_url is None
        assert updated_wikibase.article_path is None
        assert updated_wikibase.checked is False

    # Opt back in
    opt_in_result = await test_schema.execute(
        UPDATE_WIKIBASE_OPT_IN_MUTATION,
        variable_values={"wikibaseId": wikibase.id, "optIn": True},
        context_value=get_mock_context("test-auth-token"),
    )

    assert opt_in_result.errors is None
    assert opt_in_result.data is not None
    assert opt_in_result.data["updateWikibaseOptIn"] is True

    async with AsyncSession(bind=db_session) as session:
        updated_wikibase = await session.get(WikibaseModel, wikibase.id)

        assert updated_wikibase.opt_in is True
