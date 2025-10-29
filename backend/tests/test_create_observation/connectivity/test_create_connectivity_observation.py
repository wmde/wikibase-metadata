"""Test create_connectivity_observation"""

from urllib.error import HTTPError
import pytest
from fetch_data import create_connectivity_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_CONNECTIVITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchConnectivityData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.sparql
@pytest.mark.parametrize(
    ["links"],
    [
        pytest.param(
            [("Q1", "Q1")],
            marks=pytest.mark.dependency(
                name="connectivity-success-simple-1",
                depends=["connectivity-success-ood"],
                scope="session",
            ),
        ),
        pytest.param(
            [("Q1", "Q2")],
            marks=pytest.mark.dependency(
                name="connectivity-success-simple-2",
                depends=["connectivity-success-simple-1"],
                scope="session",
            ),
        ),
        pytest.param(
            [
                ("Q1", "Q2"),
                ("Q1", "Q2"),
                ("Q1", "Q2"),
                ("Q1", "Q2"),
                ("Q1", "Q2"),
                ("Q1", "Q2"),
            ],
            marks=pytest.mark.dependency(
                name="connectivity-success-simple-3",
                depends=["connectivity-success-simple-2"],
                scope="session",
            ),
        ),
        pytest.param(
            [("Q1", "Q2"), ("Q2", "Q1")],
            marks=pytest.mark.dependency(
                name="connectivity-success-simple-4",
                depends=["connectivity-success-simple-3"],
                scope="session",
            ),
        ),
        pytest.param(
            [("Q1", "Q2"), ("Q2", "Q3")],
            marks=pytest.mark.dependency(
                name="connectivity-success-simple-5",
                depends=["connectivity-success-simple-4"],
                scope="session",
            ),
        ),
    ],
)
async def test_create_connectivity_observation_success(
    mocker, links: list[tuple[str, str]]
):
    """Test"""

    returned_links = []
    for link in links:
        returned_links.append(
            {"item": {"value": link[0]}, "object": {"value": link[1]}}
        )

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_sparql_results",
        side_effect=[{"results": {"bindings": returned_links}}],
    )
    success = await create_connectivity_observation(1)
    assert success


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.dependency(
    name="connectivity-success-complex",
    depends=["connectivity-success-simple-5"],
    scope="session",
)
@pytest.mark.mutation
@pytest.mark.sparql
async def test_create_connectivity_observation_success_complex(mocker):
    """Test"""

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
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchConnectivityData"]


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.dependency(
    name="connectivity-failure",
    depends=["connectivity-success-complex"],
    scope="session",
)
@pytest.mark.sparql
async def test_create_connectivity_observation_failure(mocker):
    """Test"""

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
    success = await create_connectivity_observation(1)
    assert success is False
