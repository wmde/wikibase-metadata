"""Create Time to First Value Observation"""

import re
from requests.exceptions import HTTPError, ReadTimeout, SSLError, TooManyRedirects
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, NameResolutionError

from data import get_async_session
from fetch_data.api_data.time_to_first_value.get_creation_data import (
    get_all_creation_logs,
)
from fetch_data.api_data.time_to_first_value.get_item_namespace import (
    get_item_namespace,
)
from fetch_data.api_data.time_to_first_value.get_oldest_log import get_oldest_log_date
from fetch_data.api_data.time_to_first_value.get_revisions_data import (
    get_all_revision_logs,
)
from fetch_data.utils import get_wikibase_from_database, APIError
from logger import logger
from model.database import (
    WikibaseModel,
    WikibaseItemDateModel,
    WikibaseTimeToFirstValueObservationModel,
)

ITEM_TITLE_REGEX = re.compile(r"^Item:Q(10*)$")


async def create_time_to_first_value_observation(wikibase_id: int) -> bool:
    """Create Time to First Value Observation"""

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_time_to_first_value_observations=True,
            require_script_path=True,
        )

        logger.info("Creating TtFV Observation", extra={"wikibase": wikibase.id})

        observation = WikibaseTimeToFirstValueObservationModel(wikibase_id=wikibase.id)

        try:
            logger.debug("Fetching Creation Date", extra={"wikibase": wikibase.id})
            observation.initiation_date = await get_oldest_log_date(wikibase)

            logger.debug(f"Fetching Creation Logs", extra={"wikibase": wikibase.id})
            all_creation_logs = await get_all_creation_logs(
                api_url=wikibase.action_api_url()
            )

            logger.debug("Fetching Namespace", extra={"wikibase": wikibase.id})
            namespace_id = await get_item_namespace(wikibase)

            logger.debug(f"Fetching Revisions", extra={"wikibase": wikibase.id})
            all_revision_logs = await get_all_revision_logs(
                api_url=wikibase.action_api_url(), namespace_id=namespace_id
            )

            found = set()
            for creation in all_creation_logs:
                if (q_match := ITEM_TITLE_REGEX.match(creation.title)) is not None:
                    found.add(creation.title)
                    addition = WikibaseItemDateModel(
                        item_number=int(q_match.group(1)),
                        creation_date=creation.log_date,
                    )
                    observation.item_date_models.append(addition)
            for revision in all_revision_logs:
                if (
                    q_match := ITEM_TITLE_REGEX.match(revision.title)
                ) is not None and revision.title not in found:
                    found.add(revision.title)
                    addition = WikibaseItemDateModel(
                        item_number=int(q_match.group(1)),
                        creation_date=revision.log_date,
                    )
                    observation.item_date_models.append(addition)

            observation.returned_data = True
        except (
            ConnectTimeoutError,
            ConnectionError,
            MaxRetryError,
            NameResolutionError,
            ReadTimeout,
            SSLError,
            TooManyRedirects,
            APIError,
        ):
            logger.error("SuspectWikibaseOfflineError", extra={"wikibase": wikibase.id})
            observation.returned_data = False
        except (AssertionError, HTTPError, ValueError) as e:
            logger.warning(
                f"TimeToFirstValueDataError: {e}",
                # exc_info=True,
                # stack_info=True,
                extra={"wikibase": wikibase.id},
            )
            observation.returned_data = False

        wikibase.time_to_first_value_observations.append(observation)

        await async_session.commit()

        logger.debug(
            "TimeToFirstValue: Observation returned data: "
            + str(observation.returned_data),
            extra={"wikibase": wikibase_id},
        )
        return observation.returned_data
