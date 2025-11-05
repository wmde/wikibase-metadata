"""Test Upsert Cloud Instances"""

import os
import pytest
from sqlalchemy import select

from data.database_connection import get_async_session
from fetch_data import update_cloud_instances
from model.database import WikibaseModel, WikibaseURLModel
from model.enum import WikibaseType
from tests.test_upsert_cloud_instances.constant import DATA_DIRECTORY
from tests.utils import MockResponse


@pytest.mark.dependency(name="insert-cloud-instances", scope="session")
@pytest.mark.asyncio
async def test_insert_cloud_instances(mocker):
    """
    test updating the local database with a single cloud instance fetched from the API

    the creation of a new entry is tested
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-one.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )

        # check the wikibase instance is NOT in the database
        async with get_async_session() as async_session:
            search = "%tcdict.wikibase.cloud%"
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url.like(search))
            )
            found = (await async_session.scalars(stmt)).one_or_none()
            assert found is None

        # update from the API
        await update_cloud_instances()

        # check the wikibase instance is in the database
        async with get_async_session() as async_session:
            search = "%tcdict.wikibase.cloud%"
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url.like(search))
            )
            found = (await async_session.scalars(stmt)).one_or_none()
            assert found is not None
            assert found.wikibase_name == "Teochew Dictionary"
            assert found.description is None
            assert found.wikibase_type == WikibaseType.CLOUD
            assert found.url.url == "https://tcdict.wikibase.cloud"
            assert found.script_path.url == "/w"
            assert found.article_path.url == "/wiki"
            assert (
                found.sparql_frontend_url.url == "https://tcdict.wikibase.cloud/query/"
            )
            assert (
                found.sparql_endpoint_url.url
                == "https://tcdict.wikibase.cloud/query/sparql"
            )


@pytest.mark.dependency(
    name="update-cloud-instances", depends=["insert-cloud-instances"], scope="session"
)
@pytest.mark.asyncio
async def test_update_cloud_instances(mocker):
    """
    test updating the local database with a single cloud instance fetched from the API
    the update of an existing entry
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-one-updated.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )

        async with get_async_session() as async_session:
            search = "%tcdict.wikibase.cloud%"
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url.like(search))
            )
            found = (await async_session.scalars(stmt)).one_or_none()
            assert found is not None

        await update_cloud_instances()

        async with get_async_session() as async_session:
            search = "%tcdict.wikibase.cloud%"
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url.like(search))
            )
            found = (await async_session.scalars(stmt)).one_or_none()
            assert found is not None
            assert found.wikibase_name == "Teochew Dictionary UPDATED"
            assert found.description == "A new description"
            assert found.wikibase_type == WikibaseType.CLOUD
            assert found.url.url == "https://tcdict.wikibase.cloud"
            assert found.script_path.url == "/w"
            assert found.article_path.url == "/wiki"
            assert (
                found.sparql_frontend_url.url == "https://tcdict.wikibase.cloud/query/"
            )
            assert (
                found.sparql_endpoint_url.url
                == "https://tcdict.wikibase.cloud/query/sparql"
            )


@pytest.mark.dependency(
    name="transform-cloud-instances",
    depends=["update-cloud-instances"],
    scope="session",
)
@pytest.mark.asyncio
async def test_transform_to_cloud_instance(mocker):
    """
    test updating the local database with a single cloud instance fetched from the API
    the update of an existing entry that was not a cloud instance before
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-one.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )

        async with get_async_session() as async_session:
            search = "%tcdict.wikibase.cloud%"
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url.like(search))
            )
            found = (await async_session.scalars(stmt)).one_or_none()
            assert found is not None
            # mark the existing instance as non-cloud instance
            found.wikibase_type = WikibaseType.SUITE
            await async_session.commit()

        # breakpoint()
        await update_cloud_instances()

        async with get_async_session() as async_session:
            search = "%tcdict.wikibase.cloud%"
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url.like(search))
            )
            found = (await async_session.scalars(stmt)).one_or_none()
            assert found is not None
            assert found.wikibase_name == "Teochew Dictionary"
            assert found.description is None
            assert found.wikibase_type == WikibaseType.CLOUD
            assert found.url.url == "https://tcdict.wikibase.cloud"
            assert found.script_path.url == "/w"
            assert found.article_path.url == "/wiki"
            assert (
                found.sparql_frontend_url.url == "https://tcdict.wikibase.cloud/query/"
            )
            assert (
                found.sparql_endpoint_url.url
                == "https://tcdict.wikibase.cloud/query/sparql"
            )
