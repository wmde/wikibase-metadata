"""Create User Data Observation"""

from http.client import IncompleteRead
from requests.exceptions import (
    ChunkedEncodingError,
    ReadTimeout,
    SSLError,
    TooManyRedirects,
)
from sqlalchemy import select
from urllib3.exceptions import (
    ConnectTimeoutError,
    MaxRetryError,
    NameResolutionError,
    ProtocolError,
)

from data import get_async_session
from fetch_data.api_data.user_data.compile_user_data import (
    compile_all_implicit_user_groups,
    compile_user_group_counts,
)
from fetch_data.api_data.user_data.constants import WIKIBASE_DEFAULT_USER_GROUPS
from fetch_data.api_data.user_data.fetch_all_user_data import get_all_user_data
from fetch_data.utils import get_wikibase_from_database
from logger import logger
from model.database import (
    WikibaseModel,
    WikibaseUserGroupModel,
    WikibaseUserObservationGroupModel,
    WikibaseUserObservationModel,
)


async def create_user_observation(wikibase_id: int) -> bool:
    """Create User Data Observation."""

    logger.debug("User: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_user_observations=True,
            require_script_path=True,
        )
        action_api_url = wikibase.action_api_url()

    observation = WikibaseUserObservationModel()

    try:
        logger.debug(
            "User: Attempting to Fetch Data",
            extra={"wikibase": wikibase_id},
        )
        site_user_data = await get_all_user_data(action_api_url)
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
        logger.error(
            "SuspectWikibaseOfflineError",
            extra={"wikibase": wikibase_id},
        )
        observation.returned_data = False
    except (ChunkedEncodingError, IncompleteRead, ProtocolError, ValueError):
        logger.warning(
            "UserDataError",
            extra={"wikibase": wikibase_id},
        )
        observation.returned_data = False

    if observation.returned_data:
        logger.debug(
            "User: Data Fetch Success",
            extra={"wikibase": wikibase_id},
        )
        observation.total_users = len(site_user_data)

        logger.debug(
            "User: Compiling Groups",
            extra={"wikibase": wikibase_id},
        )
        site_implicit_user_groups = compile_all_implicit_user_groups(site_user_data)
        site_group_counts = compile_user_group_counts(site_user_data)

    async with get_async_session() as async_session:
        existing_groups = (
            await async_session.scalars(
                select(WikibaseUserGroupModel).where(
                    WikibaseUserGroupModel.group_name.in_(site_group_counts)
                )
            )
        ).all()

        groups_by_name = {
            group.group_name: group for group in existing_groups
        }

        if observation.returned_data:
            for group, count in site_group_counts.items():
                user_group = groups_by_name.get(group)

                if user_group is None:
                    user_group = WikibaseUserGroupModel(
                        group_name=group,
                        wikibase_default_group=(
                            group in WIKIBASE_DEFAULT_USER_GROUPS
                        ),
                    )

                observation.user_group_observations.append(
                    WikibaseUserObservationGroupModel(
                        user_group=user_group,
                        user_count=count,
                        group_implicit=group in site_implicit_user_groups,
                    )
                )

        logger.debug(
            "User: Saving Data",
            extra={"wikibase": wikibase_id},
        )

        wikibase = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_user_observations=True,
            require_script_path=True,
        )

        wikibase.user_observations.append(observation)

        await async_session.commit()

    logger.debug(
        "User: Observation returned data: " + str(observation.returned_data),
        extra={"wikibase": wikibase_id},
    )

    return observation.returned_data