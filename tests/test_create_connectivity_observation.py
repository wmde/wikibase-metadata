"""Test create_connectivity_observation"""

from typing import List
from urllib.error import HTTPError
import pytest
from fetch_data import create_connectivity_observation


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.sparql
@pytest.mark.parametrize(
    ["links"],
    [
        ([],),
        ([("Q1", "Q1")],),
        ([("Q1", "Q2")],),
        (
            [
                ("Q1", "Q2"),
                ("Q1", "Q2"),
                ("Q1", "Q2"),
                ("Q1", "Q2"),
                ("Q1", "Q2"),
                ("Q1", "Q2"),
            ],
        ),
        ([("Q1", "Q2"), ("Q2", "Q1")],),
        ([("Q1", "Q2"), ("Q2", "Q3")],),
    ],
)
async def test_create_connectivity_observation_success(
    mocker, links: List[tuple[str, str]]
):
    """Test"""

    returned_links = []
    for link in links:
        returned_links.append(
            {"item": {"value": link[0]}, "object": {"value": link[1]}}
        )

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_results",
        side_effect=[
            {"results": {"bindings": returned_links}},
        ],
    )
    success = await create_connectivity_observation(1)
    assert success


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.sparql
async def test_create_connectivity_observation_success_complex(mocker):
    """Test"""

    returned_links = []
    for i in range(500):
        for o in range(i + 1, i + 5):
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
        "fetch_data.sparql_data.create_connectivity_data_observation.get_results",
        side_effect=[
            {"results": {"bindings": returned_links}},
        ],
    )
    success = await create_connectivity_observation(1)
    assert success


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.sparql
async def test_create_connectivity_observation_failure(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_results",
        side_effect=[
            HTTPError(
                url="query.test.url/sparql", code=500, msg="Error", hdrs="", fp=None
            ),
        ],
    )
    success = await create_connectivity_observation(1)
    assert success is False
