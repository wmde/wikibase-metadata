"""Create Log Observation"""

from json.decoder import JSONDecodeError
from requests.exceptions import SSLError
from data import get_async_session
from fetch_data.log_data.fetch_log_data import (
    get_log_list_from_url,
    get_log_param_string,
    get_month_log_list,
)
from fetch_data.user_data import (
    get_multiple_user_data,
    get_user_type,
    get_user_type_from_user_data,
)
from fetch_data.utils import get_wikibase_from_database
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

        try:
            print("FETCHING OLDEST LOG")
            oldest_log_list = get_log_list_from_url(
                wikibase.action_api_url.url + get_log_param_string(limit=1, oldest=True)
            )
            observation.first_log_date = oldest_log_list[0].log_date

            print("FETCHING ONE MONTH'S LOGS")
            most_recent_log_list = get_month_log_list(wikibase.action_api_url.url)

            most_recent_log = max(most_recent_log_list, key=lambda x: x.id)
            observation.last_log_date = most_recent_log.log_date
            observation.last_log_user_type = get_user_type(
                wikibase, most_recent_log.user
            )

            last_month_logs = [log for log in most_recent_log_list if log.age() <= 30]
            observation.last_month_log_count = len(last_month_logs)

            observation.last_month_user_count = len(
                last_month_users := {
                    log.user
                    for log in last_month_logs
                    if log.user is not None and "page does not exist" not in log.user
                }
            )

            if len(last_month_users) > 0:
                print("FETCHING USER DATA")
                observation.last_month_human_user_count = len(
                    [
                        u
                        for u in get_multiple_user_data(wikibase, last_month_users)
                        if get_user_type_from_user_data(u) == WikibaseUserType.USER
                    ]
                )
            else:
                observation.last_month_human_user_count = 0

            observation.returned_data = True
        except (JSONDecodeError, SSLError):
            observation.returned_data = False

        wikibase.log_observations.append(observation)

        await async_session.commit()
        return observation.returned_data
