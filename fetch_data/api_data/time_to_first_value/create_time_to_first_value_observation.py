"""Create Time to First Value Observation"""

from datetime import datetime
from typing import Optional
from requests.exceptions import HTTPError, ReadTimeout, SSLError, TooManyRedirects
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, NameResolutionError

from data import get_async_session
from fetch_data.api_data.log_data.fetch_log_data import get_log_param_string
from fetch_data.api_data.time_to_first_value.get_deleted_revisions_data import (
    get_deleted_item_q_creation_date,
    get_deleted_q_creation_date,
)
from fetch_data.api_data.time_to_first_value.get_revisions_data import (
    get_item_q_creation_date,
    get_q_creation_date,
)
from fetch_data.utils import fetch_api_data, get_wikibase_from_database
from logger import logger
from model.database import (
    WikibaseModel,
    WikibaseItemDateModel,
    WikibaseTimeToFirstValueObservationModel,
)


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
            oldest_log = await fetch_api_data(
                wikibase.action_api_url()
                + get_log_param_string(limit=1, oldest=True, prop=["timestamp"])
            )
            observation.initiation_date = datetime.strptime(
                oldest_log["query"]["logevents"][0]["timestamp"], "%Y-%m-%dT%H:%M:%SZ"
            )

            returned = True
            for exponent in range(0, 7):
                if returned or exponent < 4:
                    logger.debug(
                        f"Fetching Q{pow(10, exponent)} Date",
                        extra={"wikibase": wikibase.id},
                    )
                    returned_item_model = await get_item_range_creation_date(
                        wikibase, pow(10, exponent)
                    )
                    if returned_item_model is not None:
                        observation.item_date_models.append(returned_item_model)
                        returned = True
                    else:
                        returned = False

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
        except (AssertionError, HTTPError):
            logger.warning(
                "TimeToFirstValueDataError",
                # exc_info=True,
                # stack_info=True,
                extra={"wikibase": wikibase.id},
            )
            observation.returned_data = False

        wikibase.time_to_first_value_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


async def get_item_range_creation_date(
    wikibase: WikibaseModel, baseline_item_number: int
) -> Optional[WikibaseItemDateModel]:
    """Get Item Creation Date -- Close to Baseline #"""

    for nudge in range(0, 4):
        i = baseline_item_number + nudge
        item_creation_date = min_not_none(
            [
                await get_q_creation_date(wikibase, i),
                await get_item_q_creation_date(wikibase, i),
                await get_deleted_q_creation_date(wikibase, i),
                await get_deleted_item_q_creation_date(wikibase, i),
            ]
        )
        if item_creation_date is not None:
            return WikibaseItemDateModel(
                item_number=i, creation_date=item_creation_date
            )
    return None


def min_not_none(input_list: list[Optional[datetime]]) -> Optional[datetime]:
    """Minimum Value that Is Not None"""

    if len(filtered_list := [i for i in input_list if i is not None]) == 0:
        return None
    return min(filtered_list)
