"""Test create_ttfv_observation"""

from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fetch_data.api_data.time_to_first_value.wikibase_creation_log_model import (
    WikibaseCreationLogRecord,
)
from fetch_data.api_data.time_to_first_value.wikibse_revision_model import (
    WikibaseRevisionRecord,
)
from model.database import WikibaseTimeToFirstValueObservationModel
from tests.test_schema import test_schema
from tests.utils import get_mock_context

DATA_DIRECTORY = "tests/test_create_observation/time_to_first_value/data"

FETCH_TTFV_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchTimeToFirstValueData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_ttfv_observation_success(db_session, wikibase_fixture, mocker):
    """Test Data Returned Scenario"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseTimeToFirstValueObservationModel).where(
                WikibaseTimeToFirstValueObservationModel.wikibase_id
                == wikibase_fixture.id
            )
        )
        assert before is None

    mocker.patch(
        "fetch_data.api_data.time_to_first_value.create_time_to_first_value_observation.get_all_creation_logs",
        return_value=[
            WikibaseCreationLogRecord(
                {"logid": 250, "title": "Item:Q50", "timestamp": "2026-11-19T00:00:50Z"}
            ),
            WikibaseCreationLogRecord(
                {"logid": 5, "title": "Item:Q1", "timestamp": "2026-11-19T00:00:00Z"}
            ),
            WikibaseCreationLogRecord(
                {"logid": 50, "title": "Item:Q10", "timestamp": "2026-11-19T00:00:10Z"}
            ),
        ],
    )

    mocker.patch(
        "fetch_data.api_data.time_to_first_value.create_time_to_first_value_observation.get_item_namespace",
        return_value="120",
    )

    mocker.patch(
        "fetch_data.api_data.time_to_first_value.create_time_to_first_value_observation.get_all_revision_logs",
        return_value=[
            WikibaseRevisionRecord(
                {
                    "pageid": 5,
                    "revisions": [{"timestamp": "2026-11-19T00:00:01Z"}],
                    "title": "Item:Q1",
                }
            ),
            WikibaseRevisionRecord(
                {
                    "pageid": 6,
                    "revisions": [{"timestamp": "2026-11-19T00:00:02Z"}],
                    "title": "Item:Q2",
                }
            ),
            WikibaseRevisionRecord(
                {
                    "pageid": 105,
                    "revisions": [{"timestamp": "2026-11-19T00:01:40Z"}],
                    "title": "Item:Q100",
                }
            ),
        ],
    )

    mocker.patch(
        "fetch_data.api_data.time_to_first_value.create_time_to_first_value_observation.get_oldest_log_date",
        return_value=datetime(2012, 10, 26, 20, 5, 9, tzinfo=timezone.utc),
    )

    result = await test_schema.execute(
        FETCH_TTFV_MUTATION,
        variable_values={"wikibaseId": wikibase_fixture.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchTimeToFirstValueData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseTimeToFirstValueObservationModel).where(
                WikibaseTimeToFirstValueObservationModel.wikibase_id
                == wikibase_fixture.id
            )
        )
        assert after.initiation_date == datetime(
            2012, 10, 26, 20, 5, 9, tzinfo=timezone.utc
        )
        assert len(after.item_date_models) == 4
