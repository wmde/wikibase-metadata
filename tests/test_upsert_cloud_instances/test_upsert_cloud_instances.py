"""Test create_special_statistics_observation"""

import os
import pytest
from sqlalchemy import select

from data.database_connection import get_async_session
from fetch_data import fetch_cloud_instances, update_cloud_instances
from model.database import WikibaseModel, WikibaseURLModel
from model.enum import WikibaseType
from tests.test_schema import test_schema
from tests.utils import get_mock_context, MockResponse


DATA_DIRECTORY = "tests/test_upsert_cloud_instances/data"


@pytest.mark.asyncio
async def test_fetch_cloud_instances(mocker):
    """
    test fetching a long list of cloud instances and
    examine some examples if their values are correctly parsed
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-all.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )

        instances = await fetch_cloud_instances()

        assert instances
        assert len(instances) == 8

        assert instances[0].id == 167
        assert instances[0].sitename == "Doelgericht Digitaal Transformeren"
        assert instances[0].domain == "osloddt.wikibase.cloud"
        assert instances[0].domain_decoded == "osloddt.wikibase.cloud"
        assert instances[0].description is None

        assert instances[7].id == 326
        assert instances[7].sitename == "MetaBase"
        assert instances[7].domain == "metabase.wikibase.cloud"
        assert instances[7].domain_decoded == "metabase.wikibase.cloud"
        assert instances[7].description is None


@pytest.mark.asyncio
async def test_fetch_cloud_instances_broken_response(mocker):
    """
    test fetching a list with one broken cloud instance and
    examine the remaining correct instance
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-broken.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )

        instances = await fetch_cloud_instances()

        assert instances
        assert len(instances) == 1
        assert instances[0].id == 32


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

            existing_instance = WikibaseModel(
                wikibase_name="Teochew Dictionary Self-hosted",
                base_url="https://tcdict.wikibase.cloud",
            )
            existing_instance.wikibase_type = WikibaseType.SUITE

            async_session.add(existing_instance)

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


WIKIBASE_LIST_QUERY = """
query MyQuery {
  wikibaseList(pageNumber: 1, pageSize: 10000) {
    data {
      id
      urls {
        baseUrl
      }
    }
  }
}
"""


@pytest.mark.dependency(
    name="query-cloud-instances", depends=["transform-cloud-instances"], scope="session"
)
@pytest.mark.asyncio
async def test_query_cloud_instance():
    """
    test whether querying the wikibase list via graphql returns a cloud instance
    """
    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY, context_value=get_mock_context("test-auth-token")
    )
    assert result.errors is None
    assert result.data is not None
    data = result.data
    assert "wikibaseList" in data
    wikibase_list = data["wikibaseList"]
    assert "data" in wikibase_list
    wikibase_list_data = wikibase_list["data"]

    found = [
        wikibase
        for wikibase in wikibase_list_data
        if wikibase["urls"]["baseUrl"] == "https://tcdict.wikibase.cloud"
    ]
    assert len(found) == 1
