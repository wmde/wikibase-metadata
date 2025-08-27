"""Create Time to First Value Observation"""

from datetime import datetime
from typing import Iterable, Optional
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

    for nudge in range(0, 9):
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


async def get_q_creation_date(
    wikibase: WikibaseModel, item_number: int
) -> Optional[datetime]:
    """Get Q# Creation Date"""

    try:
        rev_result = await fetch_api_data(
            wikibase.action_api_url()
            + get_revision_param_string(titles=[f"Q{item_number}"], prop=["timestamp"])
        )
        return parse_revision_timestamp(rev_result)
    except HTTPError:
        return None


async def get_item_q_creation_date(
    wikibase: WikibaseModel, item_number: int
) -> Optional[datetime]:
    """Get Item:Q# Creation Date"""

    try:
        rev_result = await fetch_api_data(
            wikibase.action_api_url()
            + get_revision_param_string(
                titles=[f"Item:Q{item_number}"], prop=["timestamp"]
            )
        )
        return parse_revision_timestamp(rev_result)
    except HTTPError:
        return None


def get_revision_param_string(
    titles: list[str],
    limit: int = 1,
    oldest: bool = True,
    prop: Optional[list[str]] = None,
) -> str:
    """Revision URL Parameters"""

    parameters: dict = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": "|".join(titles),
        "rvdir": "newer" if oldest else "older",
        # "formatversion": 2,
        "rvlimit": limit,
    }
    if prop is not None:
        parameters["rvprop"] = "|".join(prop)
    return dict_to_url(parameters)


def parse_revision_timestamp(revision_result: dict) -> Optional[datetime]:
    """Parse Timestamp from Revision"""

    try:
        rev_page_id_list: Iterable[str] = revision_result["query"]["pages"].keys()
        assert len(rev_page_id_list) > 0
        for id in rev_page_id_list:
            if "revisions" in revision_result["query"]["pages"][id]:
                item_creation_date = datetime.strptime(
                    revision_result["query"]["pages"][id]["revisions"][0][
                        "timestamp"
                    ],
                    "%Y-%m-%dT%H:%M:%SZ",
                )
                return item_creation_date
    except KeyError as exc:
        logger.debug(revision_result)
        raise exc
    return None


async def get_deleted_q_creation_date(
    wikibase: WikibaseModel, item_number: int
) -> Optional[datetime]:
    """Get Deleted Q# Creation Date"""

    try:
        del_rev_result = await fetch_api_data(
            wikibase.action_api_url()
            + get_del_rev_param_string(titles=[f"Q{item_number}"], prop=["timestamp"])
        )
        return parse_del_rev_timestamp(del_rev_result)
    except HTTPError:
        return None


async def get_deleted_item_q_creation_date(
    wikibase: WikibaseModel, item_number: int
) -> Optional[datetime]:
    """Get Deleted Item:Q# Creation Date"""

    try:
        del_rev_result = await fetch_api_data(
            wikibase.action_api_url()
            + get_del_rev_param_string(
                titles=[f"Item:Q{item_number}"], prop=["timestamp"]
            )
        )
        return parse_del_rev_timestamp(del_rev_result)
    except HTTPError:
        return None


def get_del_rev_param_string(
    titles: list[str],
    limit: int = 1,
    oldest: bool = True,
    prop: Optional[list[str]] = None,
) -> str:
    """Deleted Revision URL Parameters"""

    parameters: dict = {
        "action": "query",
        "format": "json",
        "prop": "deletedrevisions",
        "titles": "|".join(titles),
        "drvdir": "newer" if oldest else "older",
        # "formatversion": 2,
        "drvlimit": limit,
    }
    if prop is not None:
        parameters["drvprop"] = "|".join(prop)
    return dict_to_url(parameters)


def parse_del_rev_timestamp(del_rev_result: dict) -> Optional[datetime]:
    """Parse Timestamp from Deleted Revision"""

    try:
        del_rev_page_id_list: Iterable[str] = del_rev_result["query"]["pages"].keys()
        assert len(del_rev_page_id_list) > 0
        for id in del_rev_page_id_list:
            if "deletedrevisions" in del_rev_result["query"]["pages"][id]:
                item_creation_date = datetime.strptime(
                    del_rev_result["query"]["pages"][id]["deletedrevisions"][0][
                        "timestamp"
                    ],
                    "%Y-%m-%dT%H:%M:%SZ",
                )
                return item_creation_date
    except KeyError as exc:
        logger.debug(del_rev_result)
        raise exc
    return None


def min_not_none(input_list: list[Optional[datetime]]) -> Optional[datetime]:
    """Minimum Value that Is Not None"""

    if len(filtered_list := [i for i in input_list if i is not None]) == 0:
        return None
    return min(filtered_list)
