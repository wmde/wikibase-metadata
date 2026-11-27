import re

import pytest
from requests import ReadTimeout
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseAPIQuantityObservationModel
from tests.test_schema import test_schema
from tests.utils import MockResponse, get_mock_context

DATA_DIRECTORY = "tests/test_create_observation/api_quantity/data"

ALL_PAGES_API_URL = re.compile(
    r"^https://example\.com/w/api\.php\?action=query&list=allpages&apnamespace=(\d+)&aplimit=max&format=json(|&apcontinue=Q\d+)$"
)
NAMESPACE_API_URL = re.compile(
    r"^https://example\.com/w/api\.php\?action=query&meta=siteinfo&siprop=namespaces&format=json$"
)


FETCH_API_QUANTITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchApiQuantityData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_api_quantity_observation_success(
    db_session, wikibase_with_script_path, mocker
):
    """Test Data Returned Scenario"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseAPIQuantityObservationModel).where(
                WikibaseAPIQuantityObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert before is None

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (all_pages_match := ALL_PAGES_API_URL.match(query)) is not None:
            if all_pages_match.group(1) == "120":
                with open(f"{DATA_DIRECTORY}/allpages/items.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
            if all_pages_match.group(1) == "146":
                with open(f"{DATA_DIRECTORY}/allpages/lexemes.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
            if all_pages_match.group(1) == "122":
                with open(
                    f"{DATA_DIRECTORY}/allpages/properties.json", mode="rb"
                ) as data:
                    return MockResponse(query, 200, data.read())
        if NAMESPACE_API_URL.match(query) is not None:
            with open(f"{DATA_DIRECTORY}/namespaces/full.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    result = await test_schema.execute(
        FETCH_API_QUANTITY_MUTATION,
        variable_values={"wikibaseId": wikibase_with_script_path.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchApiQuantityData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseAPIQuantityObservationModel).where(
                WikibaseAPIQuantityObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert after is not None
        assert after.total_items == 10
        assert after.total_lexemes == 7
        assert after.total_properties == 5


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_api_quantity_observation_only_items(
    db_session, wikibase_with_script_path, mocker
):
    """Test Data Returned Scenario"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseAPIQuantityObservationModel).where(
                WikibaseAPIQuantityObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert before is None

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (all_pages_match := ALL_PAGES_API_URL.match(query)) is not None:
            if all_pages_match.group(1) == "120":
                with open(f"{DATA_DIRECTORY}/allpages/items.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
        if NAMESPACE_API_URL.match(query) is not None:
            with open(f"{DATA_DIRECTORY}/namespaces/items.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    result = await test_schema.execute(
        FETCH_API_QUANTITY_MUTATION,
        variable_values={"wikibaseId": wikibase_with_script_path.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchApiQuantityData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseAPIQuantityObservationModel).where(
                WikibaseAPIQuantityObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert after is not None
        assert after.total_items == 10
        assert after.total_lexemes == None
        assert after.total_properties == None


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_api_quantity_observation_only_lexemes(
    db_session, wikibase_with_script_path, mocker
):
    """Test Data Returned Scenario"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseAPIQuantityObservationModel).where(
                WikibaseAPIQuantityObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert before is None

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (all_pages_match := ALL_PAGES_API_URL.match(query)) is not None:
            if all_pages_match.group(1) == "146":
                with open(f"{DATA_DIRECTORY}/allpages/lexemes.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
        if NAMESPACE_API_URL.match(query) is not None:
            with open(f"{DATA_DIRECTORY}/namespaces/lexemes.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    result = await test_schema.execute(
        FETCH_API_QUANTITY_MUTATION,
        variable_values={"wikibaseId": wikibase_with_script_path.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchApiQuantityData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseAPIQuantityObservationModel).where(
                WikibaseAPIQuantityObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert after is not None
        assert after.total_items == None
        assert after.total_lexemes == 7
        assert after.total_properties == None


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_api_quantity_observation_only_properties(
    db_session, wikibase_with_script_path, mocker
):
    """Test Data Returned Scenario"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseAPIQuantityObservationModel).where(
                WikibaseAPIQuantityObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert before is None

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (all_pages_match := ALL_PAGES_API_URL.match(query)) is not None:
            if all_pages_match.group(1) == "122":
                with open(
                    f"{DATA_DIRECTORY}/allpages/properties.json", mode="rb"
                ) as data:
                    return MockResponse(query, 200, data.read())
        if NAMESPACE_API_URL.match(query) is not None:
            with open(
                f"{DATA_DIRECTORY}/namespaces/properties.json", mode="rb"
            ) as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    result = await test_schema.execute(
        FETCH_API_QUANTITY_MUTATION,
        variable_values={"wikibaseId": wikibase_with_script_path.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchApiQuantityData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseAPIQuantityObservationModel).where(
                WikibaseAPIQuantityObservationModel.wikibase_id
                == wikibase_with_script_path.id
            )
        )
        assert after is not None
        assert after.total_items == None
        assert after.total_lexemes == None
        assert after.total_properties == 5


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_api_quantity_observation_read_error(
    wikibase_with_script_path, mocker
):
    """Test Read Error Scenario"""

    mocker.patch(
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[ReadTimeout()],
    )

    result = await test_schema.execute(
        FETCH_API_QUANTITY_MUTATION,
        variable_values={"wikibaseId": wikibase_with_script_path.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchApiQuantityData"] is False
