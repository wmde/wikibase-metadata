"""Get Deleted Revisions Data"""

from datetime import datetime
from typing import Iterable, Optional
from requests.exceptions import HTTPError

from fetch_data.utils import dict_to_url, fetch_api_data
from logger import logger
from model.database import WikibaseModel


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
        for page_id in del_rev_page_id_list:
            if "deletedrevisions" in del_rev_result["query"]["pages"][page_id]:
                item_creation_date = datetime.strptime(
                    del_rev_result["query"]["pages"][page_id]["deletedrevisions"][0][
                        "timestamp"
                    ],
                    "%Y-%m-%dT%H:%M:%SZ",
                )
                return item_creation_date
    except KeyError as exc:
        logger.debug(del_rev_result)
        raise exc
    return None
