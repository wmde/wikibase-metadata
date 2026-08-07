"""Test create_connectivity_observation"""

from urllib.error import HTTPError

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fetch_data import create_connectivity_observation
from model.database import WikibaseConnectivityObservationModel
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_CONNECTIVITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchConnectivityData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.sparql
async def test_create_connectivity_observation_success(
    db_session, wikibase_fixture, mocker
):
    """Test"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseConnectivityObservationModel).where(
                WikibaseConnectivityObservationModel.wikibase_id == wikibase_fixture.id
            )
        )
        assert before is None

    returned_links = [{"item": {"value": "Q1"}, "object": {"value": "Q1"}}]

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_sparql_results",
        side_effect=[{"results": {"bindings": returned_links}}],
    )
    success = await create_connectivity_observation(wikibase_fixture.id)
    assert success

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseConnectivityObservationModel).where(
                WikibaseConnectivityObservationModel.wikibase_id == wikibase_fixture.id
            )
        )
        assert after is not None
        assert after.returned_data is True
        assert after.returned_links == 1
        assert after.connectivity is None
        assert after.average_connected_distance is None


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.mutation
@pytest.mark.sparql
async def test_create_connectivity_observation_success_complex(
    db_session, wikibase_fixture, mocker
):
    """Test"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseConnectivityObservationModel).where(
                WikibaseConnectivityObservationModel.wikibase_id == wikibase_fixture.id
            )
        )
        assert before is None

    returned_links = []
    for i in range(500):
        for o in range(i + 1, min(500, i + 5)):
            returned_links.append(
                {"item": {"value": f"Q{i}"}, "object": {"value": f"Q{o}"}}
            )
        for o in range(i + 1, 500, 200):
            returned_links.append(
                {"item": {"value": f"Q{i}"}, "object": {"value": f"Q{o}"}}
            )
        for o in range(0, i, 50):
            returned_links.append(
                {"item": {"value": f"Q{i}"}, "object": {"value": f"Q{o}"}}
            )

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_sparql_results",
        side_effect=[{"results": {"bindings": returned_links}}],
    )

    result = await test_schema.execute(
        FETCH_CONNECTIVITY_MUTATION,
        variable_values={"wikibaseId": wikibase_fixture.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchConnectivityData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseConnectivityObservationModel).where(
                WikibaseConnectivityObservationModel.wikibase_id == wikibase_fixture.id
            )
        )

        assert after is not None
        assert after.connectivity == 1.0
        assert after.average_connected_distance == 7.4289498997995995
        assert len(after.item_relationship_count_observations) == 9
        assert len(after.object_relationship_count_observations) == 16


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.sparql
async def test_create_connectivity_observation_failure(
    db_session, wikibase_fixture, mocker
):
    """Test"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseConnectivityObservationModel).where(
                WikibaseConnectivityObservationModel.wikibase_id == wikibase_fixture.id
            )
        )
        assert before is None

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_sparql_results",
        side_effect=[
            HTTPError(
                url="https://query.example.com/sparql",
                code=500,
                msg="Error",
                hdrs="",
                fp=None,
            )
        ],
    )
    success = await create_connectivity_observation(wikibase_fixture.id)
    assert success is False

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseConnectivityObservationModel).where(
                WikibaseConnectivityObservationModel.wikibase_id == wikibase_fixture.id
            )
        )
        assert after is not None
        assert after.returned_data is False
