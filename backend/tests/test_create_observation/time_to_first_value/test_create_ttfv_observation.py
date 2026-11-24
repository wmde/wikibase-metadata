"""Test create_ttfv_observation"""

from datetime import datetime, timezone
import re

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseTimeToFirstValueObservationModel
from tests.test_schema import test_schema
from tests.utils import MockResponse, get_mock_context

DATA_DIRECTORY = "tests/test_create_observation/time_to_first_value/data"

FETCH_TTFV_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchTimeToFirstValueData(wikibaseId: $wikibaseId)
}"""

ALL_REVISION_API_URL = re.compile(
    # pylint: disable-next=line-too-long
    r"^https://example\.com/w/api\.php\?action=query&format=json&list=allrevisions&arvnamespace=(\d+)&arvdir=newer&arvlimit=max&arvprop=ids\|title\|timestamp(|&arvcontinue=\d+\|\d+)$"
)
CREATION_LOG_API_URL = re.compile(
    # pylint: disable-next=line-too-long
    r"^https://example\.com/w/api\.php\?action=query&format=json&list=logevents&letype=create&ledir=newer&lelimit=max&leprop=ids\|title\|timestamp&letitle=Item:(Q\d+)$"
)
NAMESPACE_API_URL = re.compile(
    r"^https://example\.com/w/api\.php\?action=query&meta=siteinfo&siprop=namespaces&format=json$"
)
OLDEST_LOG_API_URL = re.compile(
    # pylint: disable-next=line-too-long
    r"^https://example\.com/w/api\.php\?action=query&format=json&list=logevents&formatversion=2&ledir=newer&lelimit=1&leprop=timestamp$"
)


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_ttfv_observation_success(
    db_session, wikibase_with_script_path, mocker
):
    """Test Data Returned Scenario"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseTimeToFirstValueObservationModel).where(
                WikibaseTimeToFirstValueObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert before is None

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (creation_log_match := CREATION_LOG_API_URL.match(query)) is not None:
            try:
                with open(
                    f"{DATA_DIRECTORY}/creation/{creation_log_match.group(1)}.json",
                    mode="rb",
                ) as data:
                    return MockResponse(query, 200, data.read())
            except FileNotFoundError:
                with open(f"{DATA_DIRECTORY}/creation/empty.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
        if (OLDEST_LOG_API_URL.match(query)) is not None:
            with open(f"{DATA_DIRECTORY}/oldest_log/success.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    result = await test_schema.execute(
        FETCH_TTFV_MUTATION,
        variable_values={"wikibaseId": wikibase_with_script_path.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchTimeToFirstValueData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseTimeToFirstValueObservationModel).where(
                WikibaseTimeToFirstValueObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert after.initiation_date == datetime(
            2026, 11, 19, 0, 0, 0, tzinfo=timezone.utc
        )
        assert len(after.item_date_models) == 5


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_ttfv_observation_success_missing_values(
    db_session, wikibase_with_script_path, mocker
):
    """Test Data Returned Scenario"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseTimeToFirstValueObservationModel).where(
                WikibaseTimeToFirstValueObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert before is None

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (all_revision_match := ALL_REVISION_API_URL.match(query)) is not None:
            assert all_revision_match.group(1) == "120"
            if all_revision_match.group(2) == "":
                with open(f"{DATA_DIRECTORY}/revision/page_1.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
            else:
                with open(
                    f"{DATA_DIRECTORY}/revision/page_2_100.json", mode="rb"
                ) as data:
                    return MockResponse(query, 200, data.read())
        if (creation_log_match := CREATION_LOG_API_URL.match(query)) is not None:
            try:
                if creation_log_match.group(1) not in ["Q50", "Q1", "Q10"]:
                    raise FileNotFoundError()
                with open(
                    f"{DATA_DIRECTORY}/creation/{creation_log_match.group(1)}.json",
                    mode="rb",
                ) as data:
                    return MockResponse(query, 200, data.read())
            except FileNotFoundError:
                with open(f"{DATA_DIRECTORY}/creation/empty.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
        if (NAMESPACE_API_URL.match(query)) is not None:
            with open(f"{DATA_DIRECTORY}/namespace/success.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())
        if (OLDEST_LOG_API_URL.match(query)) is not None:
            with open(f"{DATA_DIRECTORY}/oldest_log/success.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    result = await test_schema.execute(
        FETCH_TTFV_MUTATION,
        variable_values={"wikibaseId": wikibase_with_script_path.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchTimeToFirstValueData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseTimeToFirstValueObservationModel).where(
                WikibaseTimeToFirstValueObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert after.initiation_date == datetime(
            2026, 11, 19, 0, 0, 0, tzinfo=timezone.utc
        )
        assert len(after.item_date_models) == 4
