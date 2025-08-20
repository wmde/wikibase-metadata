"""Test update_out_of_date_recent_changes_observations"""

from datetime import datetime
import pytest
from sqlalchemy import select

from data.database_connection import get_async_session
from fetch_data import update_out_of_date_recent_changes_observations
from fetch_data.api_data.recent_changes_data import WikibaseRecentChangeRecord
from model.database import WikibaseRecentChangesObservationModel


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="recent-changes-success-ood",
    depends=["add-wikibase", "add-wikibase-script-path"],
    scope="session",
)
async def test_update_out_of_date_recent_changes_observations_success(mocker):
    """Test success scenario"""

    mock_changes_human = [
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 1, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 1,
                "user": "UserA",
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 2, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 2,
                "user": "UserB",
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 3, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 1,
                "user": "UserA",
            }
        ),
        WikibaseRecentChangeRecord(  # an anonymous user
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 4, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": "127.0.0.1",
                "userid": 0,
                "anon": "",
            }
        ),
        WikibaseRecentChangeRecord(  # userhidden, so no 'user' field
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 5, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 3,
                "userhidden": "",
            }
        ),
    ]

    mock_changes_bots = [
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 1, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 1001,
                "user": "BOT_USER_1",
            }
        ),
    ]
    mocker.patch(
        "fetch_data.api_data.recent_changes_data.create_recent_changes_observation.get_recent_changes_list",
        side_effect=[
            mock_changes_human,
            mock_changes_bots,
        ],
    )

    assert await update_out_of_date_recent_changes_observations() == 1

    async with get_async_session() as async_session:
        query = (
            select(WikibaseRecentChangesObservationModel)
            .where(WikibaseRecentChangesObservationModel.wikibase_id == 1)
            .order_by(WikibaseRecentChangesObservationModel.observation_date.desc())
        )
        observation = (await async_session.scalars(query)).first()
        assert observation is not None
        assert observation.human_change_count == 5
        assert (
            observation.human_change_user_count == 4
        )  # User:A, User:B, 127.0.0.1, __generated_user_string__user:3
        assert observation.bot_change_count == 1
        assert observation.bot_change_user_count == 1
        assert observation.first_change_date == datetime(2024, 3, 1, 12, 0, 0)
        assert observation.last_change_date == datetime(2024, 3, 5, 12, 0, 0)
