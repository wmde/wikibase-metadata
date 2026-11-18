"""
Testing services for updating Wikibases
"""

from unittest.mock import AsyncMock
import pytest

from service.wikibase_service import delete_wikibase_observations
from model.database.wikibase_observation import (
    WikibaseConnectivityObservationModel,
    WikibaseExternalIdentifierObservationModel,
    WikibaseLogMonthObservationModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseRecentChangesObservationModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseStatisticsObservationModel,
    WikibaseTimeToFirstValueObservationModel,
    WikibaseUserObservationModel,
)


@pytest.mark.asyncio
async def test_delete_wikibase_observations():
    """Test all observations for a Wikibase are deleted."""

    session = AsyncMock()
    wikibase_id = 123

    await delete_wikibase_observations(session, wikibase_id)

    observation_models = [
        WikibaseConnectivityObservationModel,
        WikibaseExternalIdentifierObservationModel,
        WikibaseLogMonthObservationModel,
        WikibasePropertyPopularityObservationModel,
        WikibaseQuantityObservationModel,
        WikibaseRecentChangesObservationModel,
        WikibaseSoftwareVersionObservationModel,
        WikibaseStatisticsObservationModel,
        WikibaseTimeToFirstValueObservationModel,
        WikibaseUserObservationModel,
    ]

    assert session.execute.await_count == len(observation_models)

    # For each observation type, check that a delete statement is generated for the wikibase
    for executed_call, model in zip(
        session.execute.await_args_list, observation_models
    ):
        statement = executed_call.args[0]

        assert statement.table == model.__table__
        assert str(statement.whereclause) == (
            f"{model.__tablename__}.wikibase_id = :wikibase_id_1"
        )
        assert statement.compile().params["wikibase_id_1"] == wikibase_id
