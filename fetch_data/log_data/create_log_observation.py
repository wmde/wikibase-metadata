"""Create Log Observation"""

from typing import List, Optional
from bs4 import BeautifulSoup, NavigableString
import requests
from data import get_async_session
from fetch_data.log_data.wikibase_log_record import WikibaseLogRecord
from fetch_data.user_data.fetch_single_user_data import (
    get_multiple_user_data,
    get_single_user_data,
)
from fetch_data.utils import dict_to_url, get_wikibase_from_database
from model.database import WikibaseLogObservationModel, WikibaseModel, WikibaseUserType


async def create_log_observation(wikibase_id: int) -> bool:
    """Create Software Version Observation"""

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            require_action_api=True,
            require_special_log=True,
        )

        observation = WikibaseLogObservationModel()

        limit = 500

        most_recent_log_list = get_log_list_from_url(
            wikibase.special_log_url.url + get_log_param_string(limit=limit)
        )

        most_recent_log = max(most_recent_log_list, key=lambda x: x.id)
        observation.last_log_date = most_recent_log.log_date
        observation.last_log_user_type = get_user_type(wikibase, most_recent_log.user)

        last_month_logs = [log for log in most_recent_log_list if log.age() <= 30]
        observation.last_month_log_count = len(last_month_logs)

        if observation.last_month_log_count == limit:
            raise ValueError("SUSPECT SHOULD FETCH ADDITIONAL PAGE")

        observation.last_month_user_count = len(
            last_month_users := {
                log.user
                for log in last_month_logs
                if "page does not exist" not in log.user
            }
        )
        observation.last_month_human_user_count = len(
            [
                u
                for u in get_multiple_user_data(wikibase, last_month_users)
                if get_user_type_from_user_data(u) == WikibaseUserType.USER
            ]
        )

        oldest_log_list = get_log_list_from_url(
            wikibase.special_log_url.url + get_log_param_string(limit=1, oldest=True)
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

    parameters: dict = {"limit": limit}
    if oldest:
        parameters["dir"] = "prev"
    if offset is not None:
        parameters["offset"] = f"{offset.log_date.strftime('%Y%m%d%H%M%S')}|{offset.id}"
    return dict_to_url(parameters)


def get_log_list_from_url(url: str) -> List[WikibaseLogRecord]:
    """Get Log List from URL"""

    print(url)

    result = requests.get(url, timeout=10)
    soup = BeautifulSoup(result.content, "html.parser")
    log_list = soup.find("body").find(
        "ul", attrs={"class": "mw-logevent-loglines"}
    ) or soup.find("body").find("div", attrs={"id": "mw-content-text"}).find("ul")
    if log_list is None or isinstance(log_list, NavigableString):

        raise ValueError(f"Could Not Find Log List at URL: {url}")

    logs = [WikibaseLogRecord(log) for log in log_list.find_all("li")]
    return logs


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
    return WikibaseUserType.MISSING
