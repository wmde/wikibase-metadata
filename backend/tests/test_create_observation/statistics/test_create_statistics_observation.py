"""Test create_special_statistics_observation"""

import os
import time

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fetch_data import create_special_statistics_observation
from model.database import WikibaseModel, WikibaseStatisticsObservationModel
from tests.test_schema import test_schema
from tests.utils import get_mock_context, MockResponse

FETCH_STATISTICS_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchStatisticsData(wikibaseId: $wikibaseId)
}"""


DATA_DIRECTORY = "tests/test_create_observation/statistics/data"


@pytest.fixture
async def wikibase_with_article_path_stats(db_session):
    """Create a wikibase with article path for statistics tests"""
    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Statistics Test Wikibase",
            base_url="https://statistics-test-example.com",
            article_path="/wiki",
            reuse=True,
            wikibase_type=None,
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)
    return wikibase


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.statistics
async def test_create_statistics_observation_success(
    db_session, wikibase_with_article_path_stats, mocker
):  # pylint: disable=redefined-outer-name
    """Test Data Returned Scenario"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseStatisticsObservationModel).where(
                WikibaseStatisticsObservationModel.wikibase_id
                == wikibase_with_article_path_stats.id
            )
        )
        assert before is None

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Statistics.html"), "rb"
    ) as version_html:

        mocker.patch(
            "fetch_data.soup_data.create_statistics_data_observation.requests.get",
            side_effect=[MockResponse("", 200, version_html.read())],
        )

    result = await test_schema.execute(
        FETCH_STATISTICS_MUTATION,
        variable_values={"wikibaseId": wikibase_with_article_path_stats.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchStatisticsData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseStatisticsObservationModel).where(
                WikibaseStatisticsObservationModel.wikibase_id
                == wikibase_with_article_path_stats.id
            )
        )
        assert after.total_pages == 12655622
        assert after.content_pages == 851723
        assert after.total_files == 30
        assert after.total_edits == 36150323
        assert after.content_page_word_count_total == 27750
        assert after.total_users == 465
        assert after.active_users == 5
        assert after.total_admin == 17


@pytest.mark.asyncio
@pytest.mark.soup
@pytest.mark.statistics
async def test_create_statistics_observation_failure(
    wikibase_with_article_path_stats, mocker, db_session
):  # pylint: disable=redefined-outer-name
    """Test Failure Scenario"""

    time.sleep(1)

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseStatisticsObservationModel).where(
                WikibaseStatisticsObservationModel.wikibase_id
                == wikibase_with_article_path_stats.id
            )
        )
        assert before is None

    mocker.patch(
        "fetch_data.soup_data.create_statistics_data_observation.requests.get",
        side_effect=[MockResponse("", 500)],
    )
    success = await create_special_statistics_observation(
        wikibase_with_article_path_stats.id
    )
    assert success is False

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseStatisticsObservationModel).where(
                WikibaseStatisticsObservationModel.wikibase_id
                == wikibase_with_article_path_stats.id
            )
        )
        assert after.returned_data is False
