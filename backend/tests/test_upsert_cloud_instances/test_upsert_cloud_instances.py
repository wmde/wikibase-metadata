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


@pytest.fixture(scope="function")
async def cloud_instance_data(mocker):
    """Setup: Insert initial cloud instance data before each test"""
    
    with open(
        os.path.join(DATA_DIRECTORY, "instances-one.json"), "rb"
    ) as instances_json:
        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )
        await update_cloud_instances()


@pytest.mark.asyncio
async def test_insert_cloud_instances(cloud_instance_data):
    """Test initial cloud instance creation"""
    
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
        assert found.sparql_frontend_url.url == "https://tcdict.wikibase.cloud/query/"
        assert found.sparql_endpoint_url.url == "https://tcdict.wikibase.cloud/query/sparql"

@pytest.mark.asyncio
async def test_update_cloud_instances(mocker, cloud_instance_data):
    """Test updating an existing cloud instance"""
    
    with open(
        os.path.join(DATA_DIRECTORY, "instances-one-updated.json"), "rb"
    ) as instances_json:
        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )
        
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
            assert found.sparql_frontend_url.url == "https://tcdict.wikibase.cloud/query/"
            assert found.sparql_endpoint_url.url == "https://tcdict.wikibase.cloud/query/sparql"

@pytest.mark.asyncio
async def test_transform_to_cloud_instance(mocker, cloud_instance_data):
    """Test transforming a non-cloud instance to cloud instance"""
    async with get_async_session() as async_session:
        search = "%tcdict.wikibase.cloud%"
        stmt = (
            select(WikibaseModel)
            .join(WikibaseModel.url)
            .where(WikibaseURLModel.url.like(search))
        )
        found = (await async_session.scalars(stmt)).one_or_none()
        assert found is not None
        found.wikibase_type = WikibaseType.SUITE
        await async_session.commit()
    
    with open(
        os.path.join(DATA_DIRECTORY, "instances-one.json"), "rb"
    ) as instances_json:
        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )
        
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
            assert found.sparql_frontend_url.url == "https://tcdict.wikibase.cloud/query/"
            assert found.sparql_endpoint_url.url == "https://tcdict.wikibase.cloud/query/sparql"