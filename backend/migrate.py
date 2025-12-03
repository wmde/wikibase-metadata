"""Migrate data from A to B"""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import joinedload, sessionmaker
from tqdm import tqdm

from config import old_database_connection_string
from data.database_connection import get_async_session
from model.database import (
    WikibaseCategoryModel,
    WikibaseModel,
    WikibaseSoftwareModel,
    WikibaseSoftwareTagModel,
    WikibaseURLModel,
    WikibaseUserGroupModel,
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

WIKIBASE_ID_QUERY = select(WikibaseModel.id).limit(10)
WIKIBASE_QUERY = select(WikibaseModel).options(
    joinedload(WikibaseModel.connectivity_observations),
    joinedload(WikibaseModel.external_identifier_observations),
    joinedload(WikibaseModel.log_month_observations),
    joinedload(WikibaseModel.property_popularity_observations),
    joinedload(WikibaseModel.quantity_observations),
    joinedload(WikibaseModel.recent_changes_observations),
    joinedload(WikibaseModel.software_version_observations),
    joinedload(WikibaseModel.statistics_observations),
    joinedload(WikibaseModel.time_to_first_value_observations),
    joinedload(WikibaseModel.user_observations),
    joinedload(WikibaseModel.languages),
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
            wikibase_id_list = (await old_session.scalars(WIKIBASE_ID_QUERY)).all()
            print("Fetched ID List")
            for wikibase_id in tqdm(wikibase_id_list, desc="Wikibases"):
                wikibase = (
                    (
                        await old_session.scalars(
                            WIKIBASE_QUERY.where(WikibaseModel.id == wikibase_id)
                        )
                    )
                    .unique()
                    .one()
                )
                merged_w = await session.merge(wikibase)
                session.add(merged_w)
            await session.commit()

    async with get_old_async_session() as old_session:
        async with get_async_session() as session:
            url_data = (await old_session.scalars(select(WikibaseURLModel))).all()
            for u in tqdm(url_data, desc="URLs"):
                merged_u = await session.merge(u)
                session.add(merged_u)
            await session.commit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(main())]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
