"""Test observation update endpoints"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

OBSERVATION_ENDPOINTS = [
    (
        "/internal/update_out_of_date_connectivity_observations",
        "update_out_of_date_connectivity_observations",
    ),
    (
        "/internal/update_out_of_date_log_first_observations",
        "update_out_of_date_log_first_observations",
    ),
    (
        "/internal/update_out_of_date_log_last_observations",
        "update_out_of_date_log_last_observations",
    ),
    (
        "/internal/update_out_of_date_recent_changes_observations",
        "update_out_of_date_recent_changes_observations",
    ),
    (
        "/internal/update_out_of_date_property_observations",
        "update_out_of_date_property_observations",
    ),
    (
        "/internal/update_out_of_date_quantity_observations",
        "update_out_of_date_quantity_observations",
    ),
    (
        "/internal/update_out_of_date_software_observations",
        "update_out_of_date_software_observations",
    ),
    (
        "/internal/update_out_of_date_stats_observations",
        "update_out_of_date_stats_observations",
    ),
    (
        "/internal/update_out_of_date_time_to_first_value_observations",
        "update_out_of_date_time_to_first_value_observations",
    ),
    (
        "/internal/update_out_of_date_user_observations",
        "update_out_of_date_user_observations",
    ),
    (
        "/internal/update_out_of_date_external_identifier_observations",
        "update_out_of_date_external_identifier_observations",
    ),
]


@pytest.mark.parametrize(
    ("endpoint", "function_name"),
    OBSERVATION_ENDPOINTS,
)
def test_observation_update_endpoint(endpoint, function_name, monkeypatch):
    """Test an observation update endpoint returns its task result."""
    monkeypatch.setenv("SCHEDULER_TOKEN", "test-token")

    result = SimpleNamespace(success=3, failure=1, total=4)

    with patch(
        f"fetch_data.{function_name}",
        new_callable=AsyncMock,
    ) as mock_update:
        mock_update.return_value = result

        response = client.post(
            endpoint,
            headers={"X-Scheduler-Token": "test-token"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "success": 3,
        "failure": 1,
        "total": 4,
    }
    mock_update.assert_awaited_once()


@pytest.mark.parametrize(
    "endpoint",
    [endpoint for endpoint, _ in OBSERVATION_ENDPOINTS],
)
def test_observation_update_endpoint_rejects_invalid_token(endpoint, monkeypatch):
    """Test observation update endpoints reject invalid scheduler tokens."""
    monkeypatch.setenv("SCHEDULER_TOKEN", "correct-token")

    response = client.post(
        endpoint,
        headers={"X-Scheduler-Token": "invalid-token"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}
