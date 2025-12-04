"""Migrate data from A to B"""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import Select, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import joinedload, sessionmaker
from tqdm import tqdm

from config import old_database_connection_string
from data.database_connection import get_async_session
from model.database import (
    WikibaseCategoryModel,
    WikibaseConnectivityObservationModel,
    WikibaseExternalIdentifierObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseRecentChangesObservationModel,
    WikibaseSoftwareModel,
    WikibaseSoftwareTagModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseStatisticsObservationModel,
    WikibaseTimeToFirstValueObservationModel,
    WikibaseURLModel,
    WikibaseUserGroupModel,
    WikibaseUserObservationModel,
)

old_async_engine = create_async_engine(
    old_database_connection_string,
    pool_size=5,  # default 5
    max_overflow=10,  # default 10
    pool_timeout=120,  # default 30, but we need more time for big queries, toolforge is slow
    connect_args={"timeout": 30},  # Wait seconds for a lock before failing
)

old_async_session = sessionmaker(
    bind=old_async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_old_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get Async Session"""
    async with old_async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()


WIKIBASE_QUERY = select(WikibaseModel).options(joinedload(WikibaseModel.languages))
CONN_OBS_QUERY = select(WikibaseConnectivityObservationModel).options(
    joinedload(
        WikibaseConnectivityObservationModel.item_relationship_count_observations
    ),
    joinedload(
        WikibaseConnectivityObservationModel.object_relationship_count_observations
    ),
)
EI_OBS_QUERY = select(WikibaseExternalIdentifierObservationModel)
LOG_OBS_QUERY = select(WikibaseLogMonthObservationModel).options(
    joinedload(WikibaseLogMonthObservationModel.log_type_records),
    joinedload(WikibaseLogMonthObservationModel.user_type_records),
)
PP_OBS_QUERY = select(WikibasePropertyPopularityObservationModel).options(
    joinedload(WikibasePropertyPopularityObservationModel.property_count_observations)
)
Q_OBS_QUERY = select(WikibaseQuantityObservationModel)
RC_OBS_QUERY = select(WikibaseRecentChangesObservationModel)
SV_OBS_QUERY = select(WikibaseSoftwareVersionObservationModel).options(
    joinedload(WikibaseSoftwareVersionObservationModel.software_versions)
)
ST_OBS_QUERY = select(WikibaseStatisticsObservationModel)
TTFV_OBS_QUERY = select(WikibaseTimeToFirstValueObservationModel).options(
    joinedload(WikibaseTimeToFirstValueObservationModel.item_date_models)
)
USER_OBS_QUERY = select(WikibaseUserObservationModel).options(
    joinedload(WikibaseUserObservationModel.user_group_observations)
)

OBSERVATION_LIST: list[tuple[str, Select]] = [
    ("Connectivity Obs", CONN_OBS_QUERY),
    ("External Identifier Obs", EI_OBS_QUERY),
    ("Log Obs", LOG_OBS_QUERY),
    ("Property Obs", PP_OBS_QUERY),
    ("Quantity Obs", Q_OBS_QUERY),
    ("Recent Changes Obs", RC_OBS_QUERY),
    ("Software Obs", SV_OBS_QUERY),
    ("Stats Obs", ST_OBS_QUERY),
    ("TtFV Obs", TTFV_OBS_QUERY),
    ("User Group Obs", USER_OBS_QUERY),
]


# pylint: disable-next=too-many-locals
async def main():
    """Migrate"""

    async with get_old_async_session() as old_session:
        async with get_async_session() as session:
            category_data = (
                await old_session.scalars(select(WikibaseCategoryModel))
            ).all()
            for c in tqdm(category_data, desc="Categories"):
                merged_c = await session.merge(c)
                session.add(merged_c)
            await session.commit()

    async with get_old_async_session() as old_session:
        async with get_async_session() as session:
            software_tag_data = (
                await old_session.scalars(select(WikibaseSoftwareTagModel))
            ).all()
            for st in tqdm(software_tag_data, desc="Software Tags"):
                merged_st = await session.merge(st)
                session.add(merged_st)
            await session.commit()

    async with get_old_async_session() as old_session:
        async with get_async_session() as session:
            software_data = (
                await old_session.scalars(select(WikibaseSoftwareModel))
            ).all()
            for u in tqdm(software_data, desc="Software"):
                merged_u = await session.merge(u)
                session.add(merged_u)
            await session.commit()

    async with get_old_async_session() as old_session:
        async with get_async_session() as session:
            user_group_data = (
                await old_session.scalars(select(WikibaseUserGroupModel))
            ).all()
            await session.execute(
                insert(WikibaseUserGroupModel)
                .values(
                    [
                        {
                            "id": u.id,
                            "group_name": u.group_name,
                            "default": u.wikibase_default_group,
                        }
                        for u in user_group_data
                    ]
                )
                .on_conflict_do_nothing()
            )
            await session.commit()
    print("Added User Groups")

    async with get_old_async_session() as old_session:
        async with get_async_session() as session:
            wikibase_data = (await old_session.scalars(WIKIBASE_QUERY)).unique().all()
            for w in tqdm(wikibase_data, desc="Wikibases"):
                merged_w = await session.merge(w)
                session.add(merged_w)
            await session.commit()

    async with get_old_async_session() as old_session:
        async with get_async_session() as session:
            url_data = (await old_session.scalars(select(WikibaseURLModel))).all()
            for u in tqdm(url_data, desc="URLs"):
                merged_u = await session.merge(u)
                session.add(merged_u)
            await session.commit()

    for name, query in OBSERVATION_LIST:
        async with get_old_async_session() as old_session:
            async with get_async_session() as session:
                obs_data = (await old_session.scalars(query)).unique().all()
                for o in tqdm(obs_data, desc=name):
                    merged_o = await session.merge(o)
                    session.add(merged_o)
                await session.commit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(main())]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
