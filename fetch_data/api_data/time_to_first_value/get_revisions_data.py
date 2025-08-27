"""Fetch Revisions Data"""

from datetime import datetime
from typing import Iterable, Optional
from requests.exceptions import HTTPError

from fetch_data.utils import dict_to_url, fetch_api_data
from logger import logger
from model.database import WikibaseModel


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
        for page_id in rev_page_id_list:
            if "revisions" in revision_result["query"]["pages"][page_id]:
                item_creation_date = datetime.strptime(
                    revision_result["query"]["pages"][page_id]["revisions"][0][
                        "timestamp"
                    ],
                    "%Y-%m-%dT%H:%M:%SZ",
                )
                return item_creation_date
    except KeyError as exc:
        logger.debug(revision_result)
        raise exc
    return None
