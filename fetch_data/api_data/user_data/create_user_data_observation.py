"""Create User Data Observation"""

from requests.exceptions import ReadTimeout, SSLError, TooManyRedirects
from sqlalchemy import select
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, NameResolutionError

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
    """Create User Data Observation"""

    logger.debug("User: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_user_observations=True,
            require_script_path=True,
        )
        observation = WikibaseUserObservationModel()

        site_user_data: list[dict]
        try:
            logger.debug(
                "User: Attempting to Fetch Data", extra={"wikibase": wikibase_id}
            )
            site_user_data = await get_all_user_data(wikibase.action_api_url())
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
        except ValueError:
            logger.warning(
                "UserDataError",
                # exc_info=True,
                # stack_info=True,
                extra={"wikibase": wikibase.id},
            )
            observation.returned_data = False

        if observation.returned_data:
            logger.debug("User: Data Fetch Success", extra={"wikibase": wikibase_id})
            observation.total_users = len(site_user_data)

            logger.debug("User: Compiling Groups", extra={"wikibase": wikibase_id})
            site_implicit_user_groups = compile_all_implicit_user_groups(site_user_data)
            site_group_counts = compile_user_group_counts(site_user_data)
            for group, count in site_group_counts.items():
                observation.user_group_observations.append(
                    WikibaseUserObservationGroupModel(
                        user_group=(
                            (
                                await async_session.scalars(
                                    select(WikibaseUserGroupModel).where(
                                        WikibaseUserGroupModel.group_name == group
                                    )
                                )
                            ).one_or_none()
                            or WikibaseUserGroupModel(
                                group_name=group,
                                wikibase_default_group=(
                                    group in WIKIBASE_DEFAULT_USER_GROUPS
                                ),
                            )
                        ),
                        user_count=count,
                        group_implicit=group in site_implicit_user_groups,
                    )
                )

        logger.debug("User: Saving Data", extra={"wikibase": wikibase_id})
        wikibase.user_observations.append(observation)

        await async_session.commit()
        logger.debug("User: SQL Committed", extra={"wikibase": wikibase_id})
        return observation.returned_data
