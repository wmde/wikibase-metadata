"""Create Recent Changes Observation"""

from collections.abc import Iterable
from http.client import IncompleteRead
from json import JSONDecodeError
from requests.exceptions import ReadTimeout, SSLError, TooManyRedirects
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, NameResolutionError

from data.database_connection import get_async_session
from fetch_data.api_data.recent_changes_data.fetch_recent_changes_data import (
    get_recent_changes_list,
)
from fetch_data.api_data.recent_changes_data.wikibase_recent_change_record import (
    WikibaseRecentChangeRecord,
)
from fetch_data.utils import get_wikibase_from_database
from logger import logger
from model.database import (
    WikibaseModel,
    WikibaseRecentChangesObservationModel,
)


async def create_recent_changes_observation(wikibase_id: int) -> bool:
    """Create Recent Changes Observation"""

    logger.debug(
        "RecentChanges: Attempting Observation", extra={"wikibase": wikibase_id}
    )

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_recent_changes_observations=True,
            require_script_path=True,
        )

        observation = WikibaseRecentChangesObservationModel(wikibase_id=wikibase.id)

        try:
            logger.info(
                "Fetching Recent Changes (without bots)",
                extra={"wikibase": wikibase.id},
            )
            recent_changes_list_humans = await get_recent_changes_list(
                wikibase.action_api_url(), bots=False
            )

            logger.info(
                "Fetching Recent Changes (with bots)", extra={"wikibase": wikibase.id}
            )
            recent_changes_list_bots = await get_recent_changes_list(
                wikibase.action_api_url(), bots=True
            )

            observation = create_recent_changes(
                recent_changes_list_humans,
                recent_changes_list_bots,
                observation,
            )
            observation.returned_data = True
        except (
            ConnectTimeoutError,
            ConnectionError,
            MaxRetryError,
            NameResolutionError,
            ReadTimeout,
            SSLError,
            TooManyRedirects,
        ):
            logger.error("SuspectWikibaseOfflineError", extra={"wikibase": wikibase.id})
            observation.returned_data = False
        except (IncompleteRead, JSONDecodeError):
            logger.warning(
                "RecentChangesDataError",
                # exc_info=True,
                # stack_info=True,
                extra={"wikibase": wikibase.id},
            )
            observation.returned_data = False

        wikibase.recent_changes_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


def create_recent_changes(
    recent_changes_list_humans: Iterable[WikibaseRecentChangeRecord],
    recent_changes_list_bots: Iterable[WikibaseRecentChangeRecord],
    result: WikibaseRecentChangesObservationModel,
) -> WikibaseRecentChangesObservationModel:
    """Create Recent Changes"""

    list_humans = list(recent_changes_list_humans)
    result.human_change_count = len(list_humans)
    result.human_change_user_count = len(
        {rc.user for rc in list_humans if rc.user is not None}
    )

    list_bots = list(recent_changes_list_bots)
    result.bot_change_count = len(list_bots)
    result.bot_change_user_count = len(
        {rc.user for rc in list_bots if rc.user is not None}
    )

    list_total = [*list_humans, *list_bots]

    if len(list_total) > 0:
        result.first_change_date = min(rc.timestamp for rc in list_total)
        result.last_change_date = max(rc.timestamp for rc in list_total)

    return result
