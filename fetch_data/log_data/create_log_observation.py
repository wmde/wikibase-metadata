"""Create Log Observation"""

from datetime import datetime
from typing import List, Optional
from data import get_async_session
from fetch_data.log_data.wikibase_log_record import WikibaseLogRecord
from fetch_data.user_data.fetch_single_user_data import (
    get_multiple_user_data,
    get_single_user_data,
)
from fetch_data.utils import dict_to_url, get_wikibase_from_database
from fetch_data.utils.fetch_api_data import fetch_api_data
from model.database import WikibaseLogObservationModel, WikibaseModel, WikibaseUserType


async def create_log_observation(wikibase_id: int) -> bool:
    """Create Software Version Observation"""

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            require_action_api=True,
        )

        observation = WikibaseLogObservationModel()

        print("FETCHING ONE MONTH'S LOGS")

        most_recent_log_list = get_month_log_list(wikibase.action_api_url.url)

        most_recent_log = max(most_recent_log_list, key=lambda x: x.id)
        observation.last_log_date = most_recent_log.log_date
        observation.last_log_user_type = get_user_type(wikibase, most_recent_log.user)

        last_month_logs = [log for log in most_recent_log_list if log.age() <= 30]
        observation.last_month_log_count = len(last_month_logs)

        observation.last_month_user_count = len(
            last_month_users := {
                log.user
                for log in last_month_logs
                if "page does not exist" not in log.user
            }
        )

        print("FETCHING USER DATA")

        observation.last_month_human_user_count = len(
            [
                u
                for u in get_multiple_user_data(wikibase, last_month_users)
                if get_user_type_from_user_data(u) == WikibaseUserType.USER
            ]
        )

        oldest_log_list = get_log_list_from_url(
            wikibase.action_api_url.url + get_log_param_string(limit=1, oldest=True)
        )
        observation.first_log_date = oldest_log_list[0].log_date

        observation.returned_data = True

        wikibase.log_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


def get_log_param_string(
    limit: Optional[int] = None,
    oldest: bool = False,
    offset: Optional[WikibaseLogRecord] = None,
):
    """Log Page URL Parameters"""

    parameters: dict = {
        "action": "query",
        "format": "json",
        "list": "logevents",
        "formatversion": 2,
        "ledir": "newer" if oldest else "older",
        "lelimit": limit,
    }

    if offset is not None:
        parameters["lecontinue"] = (
            f"{offset.log_date.strftime('%Y%m%d%H%M%S')}|{offset.id}"
        )
    return dict_to_url(parameters)


def get_log_list_from_url(url: str) -> List[WikibaseLogRecord]:
    """Get Log List from URL"""

    data = []

    query_data = fetch_api_data(url)
    for record in query_data["query"]["logevents"]:
        data.append(WikibaseLogRecord(record))

    return data


def get_month_log_list(
    api_url: str,
) -> List[WikibaseLogRecord]:
    """Get Log List from api_url"""

    data: List[WikibaseLogRecord] = []
    limit = 500

    should_query = True
    next_from: Optional[WikibaseLogRecord] = None
    while should_query:
        query_data = fetch_api_data(
            api_url + get_log_param_string(limit=limit, offset=next_from)
        )
        for record in query_data["query"]["logevents"]:
            data.append(WikibaseLogRecord(record))
        should_query = (
            datetime.now() - (next_from := min(data, key=lambda x: x.log_date)).log_date
        ).days <= 30

    return data


def get_user_type(wikibase: WikibaseModel, user: str) -> WikibaseUserType:
    """User or Bot?"""

    user_data = get_single_user_data(wikibase, user)
    return get_user_type_from_user_data(user_data)


def get_user_type_from_user_data(user_data: dict) -> WikibaseUserType:
    """User or Bot?"""

    if "groups" not in user_data and "missing" in user_data:
        return WikibaseUserType.MISSING
    if "bot" in user_data["groups"]:
        return WikibaseUserType.BOT
    return WikibaseUserType.USER
