"""Create Log Observation"""

from collections.abc import Iterable
from datetime import datetime
from http.client import IncompleteRead
from json import JSONDecodeError
from requests.exceptions import (
    ChunkedEncodingError,
    ReadTimeout,
    SSLError,
    TooManyRedirects,
)
from urllib3.exceptions import (
    ConnectTimeoutError,
    MaxRetryError,
    NameResolutionError,
    ProtocolError,
)

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
from fetch_data.utils import counts, get_wikibase_from_database
from logger import logger
from model.database import (
    WikibaseLogMonthLogTypeObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseLogMonthUserTypeObservationModel,
    WikibaseModel,
)
from model.enum import WikibaseLogType, WikibaseUserType


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
        except (ChunkedEncodingError, IncompleteRead, JSONDecodeError, ProtocolError):
            logger.warning(
                "LogDataError",
                # exc_info=True,
                # stack_info=True,
                extra={"wikibase": wikibase.id},
            )
            observation.returned_data = False

        wikibase.log_month_observations.append(observation)

        await async_session.commit()

        logger.debug(
            "Log: Observation returned data: " + str(observation.returned_data),
            extra={"wikibase": wikibase_id},
        )
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

    user_counts = counts(
        log.user
        for log in log_list
        if log.user is not None and "page does not exist" not in log.user
    )

    result.user_count = len(user_counts)
    result.active_user_count = len([u for u, v in user_counts.items() if v >= 5])

    user_type_dict: dict[str, WikibaseUserType] = {}

    if len(user_counts) > 0:
        logger.info("Fetching User Data", extra={"wikibase": wikibase.id})
        user_data = await get_multiple_user_data(wikibase, user_counts.keys())
        for u in user_data:
            user_type_dict[u["name"]] = get_user_type_from_user_data(u)

        result.last_log_user_type = user_type_dict.get(
            max(log_list, key=lambda log: log.log_date).user
        )

    result.human_user_count = len(
        [
            u
            for u in user_counts.keys()
            if user_type_dict.get(u) == WikibaseUserType.USER
        ]
    )
    result.active_human_user_count = len(
        [
            u
            for u, v in user_counts.items()
            if v >= 5 and user_type_dict.get(u) == WikibaseUserType.USER
        ]
    )

    for log_type in sorted({log.log_type for log in log_list}, key=lambda x: x.value):
        log_type_record = compile_log_type_record(log_list, user_type_dict, log_type)
        result.log_type_records.append(log_type_record)

    for user_type in sorted(
        {x for log in log_list if (x := user_type_dict.get(log.user)) is not None},
        key=lambda x: x.value,
    ):
        user_type_record = compile_user_type_record(log_list, user_type_dict, user_type)
        result.user_type_records.append(user_type_record)

    return result


def compile_log_type_record(
    log_list: Iterable[WikibaseLogRecord],
    user_type_dict: dict[str, WikibaseUserType],
    log_type: WikibaseLogType,
) -> WikibaseLogMonthLogTypeObservationModel:
    """Compile Log-Type Record"""

    log_type_record = WikibaseLogMonthLogTypeObservationModel(log_type=log_type)
    log_type_record.log_count = len(
        log_type_logs := [l for l in log_list if l.log_type == log_type]
    )
    log_type_record.first_log_date = min(log.log_date for log in log_type_logs)
    log_type_record.last_log_date = max(log.log_date for log in log_type_logs)

    type_user_counts = counts(log.user for log in log_type_logs if log.user is not None)
    log_type_record.user_count = len(type_user_counts)
    log_type_record.active_user_count = len(
        [u for u, v in type_user_counts.items() if v >= 5]
    )

    log_type_record.human_user_count = len(
        [
            u
            for u in type_user_counts.keys()
            if user_type_dict.get(u) == WikibaseUserType.USER
        ]
    )
    log_type_record.active_human_user_count = len(
        [
            u
            for u, v in type_user_counts.items()
            if v >= 5 and user_type_dict.get(u) == WikibaseUserType.USER
        ]
    )

    return log_type_record


def compile_user_type_record(
    log_list: Iterable[WikibaseLogRecord],
    user_type_dict: dict[str, WikibaseUserType],
    user_type: WikibaseUserType,
) -> WikibaseLogMonthUserTypeObservationModel:
    """Compile User-Type Record"""

    user_type_record = WikibaseLogMonthUserTypeObservationModel(user_type=user_type)
    user_type_record.log_count = len(
        user_type_logs := [
            l for l in log_list if user_type_dict.get(l.user) == user_type
        ]
    )
    user_type_record.first_log_date = min(log.log_date for log in user_type_logs)
    user_type_record.last_log_date = max(log.log_date for log in user_type_logs)
    user_counts = counts(log.user for log in user_type_logs)
    user_type_record.user_count = len(user_counts)
    user_type_record.active_user_count = len(
        [u for u, v in user_counts.items() if v >= 5]
    )
    return user_type_record
