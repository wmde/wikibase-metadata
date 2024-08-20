"""Create User Data Observation"""

from requests.exceptions import ReadTimeout, SSLError
from sqlalchemy import select
from data import get_async_session
from fetch_data.api_data.user_data.compile_user_data import (
    compile_all_implicit_user_groups,
    compile_user_group_counts,
)
from fetch_data.api_data.user_data.constants import WIKIBASE_DEFAULT_USER_GROUPS
from fetch_data.api_data.user_data.fetch_all_user_data import fetch_all_user_data
from fetch_data.utils.get_wikibase import get_wikibase_from_database
from model.database import (
    WikibaseUserGroupModel,
    WikibaseUserObservationGroupModel,
    WikibaseUserObservationModel,
)
from model.database.wikibase_model import WikibaseModel


async def create_user_observation(wikibase_id: int) -> bool:
    """Create User Data Observation"""
    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            require_action_api=True,
        )
        observation = WikibaseUserObservationModel()

        site_user_data: list[dict]
        try:
            site_user_data = fetch_all_user_data(wikibase.action_api_url.url)
            observation.returned_data = True
        except (ReadTimeout, SSLError, ValueError):
            observation.returned_data = False

        if observation.returned_data:
            observation.total_users = len(site_user_data)

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

        wikibase.user_observations.append(observation)

        await async_session.commit()
        return observation.returned_data
