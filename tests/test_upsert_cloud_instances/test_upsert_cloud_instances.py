"""Test create_special_statistics_observation"""

import os
import pytest
from logger import logger
from tests.utils import MockResponse
from data import get_async_session
from sqlalchemy import select
from model.database import WikibaseModel
from model.database.wikibase_url_model import WikibaseURLModel

from fetch_data.cloud_api_data import fetch_cloud_instances, update_cloud_instances


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
        assert len(instances) == 1554

        assert instances[0].id == 167
        assert instances[0].sitename == "Doelgericht Digitaal Transformeren"
        assert instances[0].domain == "osloddt.wikibase.cloud"
        assert instances[0].domain_decoded == "osloddt.wikibase.cloud"
        assert instances[0].description == None

        assert instances[42].id == 326
        assert instances[42].sitename == "MetaBase"
        assert instances[42].domain == "metabase.wikibase.cloud"
        assert instances[42].domain_decoded == "metabase.wikibase.cloud"
        assert instances[42].description == None


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


@pytest.mark.asyncio
async def test_update_cloud_instances(mocker):
    """
    test updating the local database with a single cloud instance fetched from the API

    in a first step, the creation of a new entry is tested,
    then the update of an existing entry
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-one.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )
        MOCK_INSTANCE_DOMAIN = "osloddt.wikibase.cloud"
        MOCK_INSTANCE_NAME = "Doelgericht Digitaal Transformeren"

        async with get_async_session() as async_session:
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url == MOCK_INSTANCE_DOMAIN)
            )
            result = await async_session.execute(stmt)
            found = result.scalars().first()
            assert found is None

        await update_cloud_instances()

        async with get_async_session() as async_session:
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url == MOCK_INSTANCE_DOMAIN)
            )
            result = await async_session.execute(stmt)
            found = result.scalars().first()
            assert found is not None
            assert found.wikibase_name == MOCK_INSTANCE_NAME

    with open(
        os.path.join(DATA_DIRECTORY, "instances-one-updated.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )
        MOCK_INSTANCE_DOMAIN = "osloddt.wikibase.cloud"
        MOCK_INSTANCE_NAME_RENAMED = "Doelgericht Digitaal Transformeren RENAMED"

        async with get_async_session() as async_session:
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url == MOCK_INSTANCE_DOMAIN)
            )
            result = await async_session.execute(stmt)
            found = result.scalars().first()
            assert found is not None

        await update_cloud_instances()

        async with get_async_session() as async_session:
            stmt = (
                select(WikibaseModel)
                .join(WikibaseModel.url)
                .where(WikibaseURLModel.url == MOCK_INSTANCE_DOMAIN)
            )
            result = await async_session.execute(stmt)
            found = result.scalars().first()
            assert found is not None
            assert found.wikibase_name == MOCK_INSTANCE_NAME_RENAMED
