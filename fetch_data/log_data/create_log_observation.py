"""Create Log Observation"""

from datetime import datetime
from json.decoder import JSONDecodeError
from typing import List
from requests.exceptions import SSLError
from data import get_async_session
from fetch_data.log_data.fetch_log_data import (
    get_log_list_from_url,
    get_log_param_string,
    get_month_log_list,
)
from fetch_data.log_data.wikibase_log_record import WikibaseLogRecord
from fetch_data.user_data import (
    get_multiple_user_data,
    get_user_type,
    get_user_type_from_user_data,
)
from fetch_data.utils import get_wikibase_from_database
from model.database import (
    WikibaseLogMonthObservationModel,
    WikibaseLogMonthTypeObservationModel,
    WikibaseLogObservationModel,
    WikibaseModel,
)
from model.database.wikibase_observation.log.wikibase_log_month_user_observation_model import (
    WikibaseLogMonthUserObservationModel,
)
from model.enum import WikibaseUserType


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
            oldest_log = get_log_list_from_url(
                wikibase.action_api_url.url + get_log_param_string(limit=1, oldest=True)
            )[0]
            observation.first_log_date = oldest_log.log_date

            print("FETCHING FIRST MONTH'S LOGS")
            initial_log_list = get_month_log_list(
                wikibase.action_api_url.url,
                comparison_date=oldest_log.log_date,
                oldest=True,
            )
            first_month_log_list = [
                l
                for l in initial_log_list
                if abs((l.log_date - oldest_log.log_date).days) <= 30
            ]

            print("FETCHING LAST MONTH'S LOGS")
            most_recent_log_list = get_month_log_list(
                wikibase.action_api_url.url, comparison_date=datetime.today()
            )
            last_month_log_list = [l for l in most_recent_log_list if l.age() <= 30]

            most_recent_log = max(most_recent_log_list, key=lambda x: x.id)
            observation.last_log_date = most_recent_log.log_date
            observation.last_log_user_type = get_user_type(
                wikibase, most_recent_log.user
            )

            observation.last_month = await create_log_month(
                wikibase, last_month_log_list
            )
            observation.first_month = await create_log_month(
                wikibase, first_month_log_list
            )

            observation.returned_data = True
        except (JSONDecodeError, SSLError):
            observation.returned_data = False

        wikibase.log_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


async def create_log_month(
    wikibase: WikibaseModel,
    log_list: List[WikibaseLogRecord],
) -> WikibaseLogMonthObservationModel:
    """Create Log Month"""

    result = WikibaseLogMonthObservationModel(log_count=len(log_list))

    if len(log_list) > 0:
        result.first_log_date = min(log.log_date for log in log_list)
        result.last_log_date = max(log.log_date for log in log_list)

    result.user_count = len(
        users := {
            log.user
            for log in log_list
            if log.user is not None and "page does not exist" not in log.user
        }
    )

    user_type_dict: dict[str, WikibaseUserType] = {}

    if len(users) > 0:
        print("FETCHING USER DATA")
        user_data = get_multiple_user_data(wikibase, users)
        for u in user_data:
            user_type_dict[u["name"]] = get_user_type_from_user_data(u)

    result.human_user_count = len(
        [u for u in users if user_type_dict.get(u) == WikibaseUserType.USER]
    )

    for log_type in {log.log_type for log in log_list}:
        log_type_record = WikibaseLogMonthTypeObservationModel(log_type=log_type)
        log_type_record.log_count = len(
            type_logs := [l for l in log_list if l.log_type == log_type]
        )
        log_type_record.first_log_date = min(log.log_date for log in type_logs)
        log_type_record.last_log_date = max(log.log_date for log in type_logs)
        log_type_record.user_count = len(type_users := {log.user for log in type_logs})
        log_type_record.human_user_count = len(
            [u for u in type_users if user_type_dict.get(u) == WikibaseUserType.USER]
        )
        result.log_type_records.append(log_type_record)

    for user_type in {user_type_dict.get(log.user) for log in log_list}:
        if user_type is not None:
            user_type_record = WikibaseLogMonthUserObservationModel(user_type=user_type)
            user_type_record.log_count = len(
                type_logs := [l for l in log_list if l.log_type == log_type]
            )
            user_type_record.first_log_date = min(log.log_date for log in type_logs)
            user_type_record.last_log_date = max(log.log_date for log in type_logs)
            user_type_record.user_count = len({log.user for log in type_logs})
            result.user_type_records.append(user_type_record)
    return result
