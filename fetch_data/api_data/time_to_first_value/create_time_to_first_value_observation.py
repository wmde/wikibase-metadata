"""Create Time to First Value Observation"""

from datetime import datetime
from typing import Optional
import requests
from requests.exceptions import HTTPError, ReadTimeout, SSLError, TooManyRedirects
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, NameResolutionError

from data import get_async_session
from fetch_data.api_data.log_data.fetch_log_data import get_log_param_string
from fetch_data.utils import dict_to_url, fetch_api_data, get_wikibase_from_database
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

        observation = WikibaseTimeToFirstValueObservationModel(wikibase_id=wikibase.id)

        try:
            logger.info("Fetching Creation Date", extra={"wikibase": wikibase.id})
            oldest_log = await fetch_api_data(
                wikibase.action_api_url()
                + get_log_param_string(limit=1, oldest=True, prop=["timestamp"])
            )
            observation.initiation_date = datetime.strptime(
                oldest_log["query"]["logevents"][0]["timestamp"], "%Y-%m-%dT%H:%M:%SZ"
            )

            returned = True
            for exponent in range(0, 7):
                if returned:
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

    for nudge in range(0, 8):
        i = baseline_item_number + nudge
        item_creation_date = await get_item_creation_date(wikibase, i)
        if item_creation_date is not None:
            return WikibaseItemDateModel(
                item_number=i, creation_date=item_creation_date
            )
    return None


async def get_item_creation_date(
    wikibase: WikibaseModel, item_number: int
) -> Optional[datetime]:
    """Get Item Creation Date"""

    try:
        rev_log_result = await fetch_api_data(
            wikibase.action_api_url()
            + get_revision_param_string(
                title=f"Q{item_number}", limit=1, prop=["timestamp"]
            )
        )
        rev_page_id = [*rev_log_result["query"]["pages"].keys()][0]
        assert rev_page_id != "-1"
        item_creation_date = datetime.strptime(
            rev_log_result["query"]["pages"][rev_page_id]["revisions"][0]["timestamp"],
            "%Y-%m-%dT%H:%M:%SZ",
        )
        return item_creation_date

    except (HTTPError, AssertionError):
        return None


def get_revision_param_string(
    title: str,
    limit: Optional[int] = None,
    oldest: bool = True,
    prop: Optional[list[str]] = None,
) -> str:
    """Log Page URL Parameters"""

    parameters: dict = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "rvdir": "newer" if oldest else "older",
        # "formatversion": 2,
        "rvlimit": limit,
    }
    if prop is not None:
        parameters["rvprop"] = "|".join(prop)
    return dict_to_url(parameters)
