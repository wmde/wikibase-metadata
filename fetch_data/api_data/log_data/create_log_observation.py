"""Create Log Observation"""

from collections.abc import Iterable
from datetime import datetime
from json import JSONDecodeError
from requests.exceptions import ReadTimeout, SSLError, TooManyRedirects
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, NameResolutionError

from data.database_connection import get_async_session
from fetch_data.api_data.log_data.fetch_log_data import (
    get_log_list_from_url,
    get_log_param_string,
    get_month_log_list,
)
from fetch_data.api_data.log_data.wikibase_log_record import WikibaseLogRecord
from fetch_data.api_data.user_data import (
    get_multiple_user_data,
    get_user_type_from_user_data,
)
from fetch_data.utils import get_wikibase_from_database
from logger import logger
from model.database import (
    WikibaseLogMonthLogTypeObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseLogMonthUserTypeObservationModel,
    WikibaseModel,
)
from model.enum import WikibaseUserType


async def create_log_observation(wikibase_id: int, first_month: bool) -> bool:
    """Create Log Observation"""

    logger.debug("Log: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_log_observations=True,
            require_script_path=True,
        )

        observation = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=first_month
        )

        try:
            logger.info("Fetching Logs", extra={"wikibase": wikibase.id})
            log_list = await get_month_log_list(
                wikibase.action_api_url(),
                comparison_date=await get_log_list_comparison_date(
                    wikibase, first_month
                ),
                oldest=first_month,
            )
            observation = await create_log_month(wikibase, log_list, observation)
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
        except JSONDecodeError:
            logger.warning(
                "LogDataError",
                # exc_info=True,
                # stack_info=True,
                extra={"wikibase": wikibase.id},
            )
            observation.returned_data = False

        wikibase.log_month_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


async def get_log_list_comparison_date(
    wikibase: WikibaseModel, first: bool
) -> datetime:
    """Return either date of first log or today"""

    if first:
        logger.info("Fetching Oldest Log", extra={"wikibase": wikibase.id})
        oldest_log = (
            await get_log_list_from_url(
                wikibase.action_api_url() + get_log_param_string(limit=1, oldest=True)
            )
        )[0]
        return oldest_log.log_date

    return datetime.today()


async def create_log_month(
    wikibase: WikibaseModel,
    log_list: Iterable[WikibaseLogRecord],
    result: WikibaseLogMonthObservationModel,
) -> WikibaseLogMonthObservationModel:
    """Create Log Month"""

    result.log_count = len(log_list)

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
        logger.info("Fetching User Data", extra={"wikibase": wikibase.id})
        user_data = await get_multiple_user_data(wikibase, users)
        for u in user_data:
            user_type_dict[u["name"]] = get_user_type_from_user_data(u)

        result.last_log_user_type = user_type_dict.get(
            max(log_list, key=lambda log: log.log_date).user
        )

    result.human_user_count = len(
        [u for u in users if user_type_dict.get(u) == WikibaseUserType.USER]
    )

    for log_type in sorted({log.log_type for log in log_list}, key=lambda x: x.value):
        log_type_record = WikibaseLogMonthLogTypeObservationModel(log_type=log_type)
        log_type_record.log_count = len(
            log_type_logs := [l for l in log_list if l.log_type == log_type]
        )
        log_type_record.first_log_date = min(log.log_date for log in log_type_logs)
        log_type_record.last_log_date = max(log.log_date for log in log_type_logs)
        log_type_record.user_count = len(
            type_users := {log.user for log in log_type_logs if log.user is not None}
        )
        log_type_record.human_user_count = len(
            [u for u in type_users if user_type_dict.get(u) == WikibaseUserType.USER]
        )
        result.log_type_records.append(log_type_record)

    for user_type in sorted(
        {x for log in log_list if (x := user_type_dict.get(log.user)) is not None},
        key=lambda x: x.value,
    ):
        user_type_record = WikibaseLogMonthUserTypeObservationModel(user_type=user_type)
        user_type_record.log_count = len(
            user_type_logs := [
                l for l in log_list if user_type_dict.get(l.user) == user_type
            ]
        )
        user_type_record.first_log_date = min(log.log_date for log in user_type_logs)
        user_type_record.last_log_date = max(log.log_date for log in user_type_logs)
        user_type_record.user_count = len({log.user for log in user_type_logs})
        result.user_type_records.append(user_type_record)
    return result
