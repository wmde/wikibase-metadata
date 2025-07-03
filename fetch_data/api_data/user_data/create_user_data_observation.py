"""Create User Data Observation"""

from typing import Optional
from requests.exceptions import ReadTimeout, SSLError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from data import get_async_session
from fetch_data.api_data.user_data.compile_user_data import (
    compile_all_implicit_user_groups,
    compile_user_group_counts,
)
from fetch_data.api_data.user_data.constants import WIKIBASE_DEFAULT_USER_GROUPS
from fetch_data.api_data.user_data.fetch_all_user_data import get_all_user_data
from logger import logger
from model.database import (
    WikibaseModel,
    WikibaseUserGroupModel,
    WikibaseUserObservationGroupModel,
    WikibaseUserObservationModel,
)


async def create_user_observation(wikibase_id: int) -> bool:
    """Create User Data Observation"""

    logger.info("User: Attempting Observation", extra={"wikibase": wikibase_id})
    logger.debug("User: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        # wikibase: WikibaseModel = await get_wikibase_from_database(
        #     async_session=async_session,
        #     wikibase_id=wikibase_id,
        #     include_observations=True,
        #     require_action_api=True,
        # )
        wikibase = await fetch_wikibase(async_session, wikibase_id)
        observation = WikibaseUserObservationModel()

        site_user_data: list[dict]
        try:
            logger.debug(
                "User: Attempting to Fetch Data", extra={"wikibase": wikibase_id}
            )
            site_user_data = await get_all_user_data(wikibase.action_api_url())
            observation.returned_data = True
        except (ReadTimeout, SSLError, ValueError):
            logger.warning(
                "UserDataError",
                exc_info=True,
                stack_info=True,
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


async def fetch_wikibase(
    async_session: AsyncSession, wikibase_id: int
) -> WikibaseModel:
    """Fetch Wikibase"""

    try:
        wikibase: Optional[WikibaseModel] = (
            (
                await async_session.scalars(
                    select(WikibaseModel)
                    .options(joinedload(WikibaseModel.user_observations))
                    .where(WikibaseModel.id == wikibase_id)
                )
            )
            .unique()
            .one_or_none()
        )
    except Exception as exc:
        logger.error(exc, extra={"wikibase": wikibase_id})
        raise exc
    try:
        assert wikibase is not None
        assert wikibase.action_api_url() is not None
    except AssertionError as exc:
        logger.error(exc, extra={"wikibase": wikibase_id})
        raise exc

    logger.debug("User: Retrieved Wikibase", extra={"wikibase": wikibase_id})
    return wikibase
