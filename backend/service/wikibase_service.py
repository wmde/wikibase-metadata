from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

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


async def delete_wikibase_observations(session: AsyncSession, wikibase_id: int):
    """Delete all observations for a Wikibase."""

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

    for model in observation_models:
        await session.execute(delete(model).where(model.wikibase_id == wikibase_id))
