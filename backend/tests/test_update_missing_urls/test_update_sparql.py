"""Test Update Missing SPARQL Urls"""

from datetime import datetime, timezone

import pytest

from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.version.software_version_model import (
    WikibaseSoftwareVersionModel,
)
from model.database.wikibase_observation.version.wikibase_version_observation_model import (
    WikibaseSoftwareVersionObservationModel,
)
from model.database.wikibase_software.software_model import WikibaseSoftwareModel
from model.enum.wikibase_software_type_enum import WikibaseSoftwareType
from resolvers.update import update_missing_sparql_urls
from tests.test_schema import test_schema
from tests.test_update_missing_urls.constant import DATA_DIRECTORY, WIKIBASE_URLS_QUERY
from tests.utils import MockResponse, assert_layered_property_value


@pytest.fixture
async def wikibase_with_manifest(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with WikibaseManifest software version observation"""
    async with get_async_session() as session:
        manifest_software = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="WikibaseManifest",
        )
        session.add(manifest_software)
        await session.flush()
        await session.refresh(manifest_software)

        wikibase = WikibaseModel(
            wikibase_name="Manifest Test Wikibase",
            base_url="https://mock-wikibase.com",
            script_path="/mockwiki",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseSoftwareVersionObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs)
        await session.flush()
        await session.refresh(obs)

        version = WikibaseSoftwareVersionModel(
            software=manifest_software,
            version="0.0.1",
        )
        version.wikibase_software_version_observation_id = obs.id
        session.add(version)
        await session.flush()

        wikibase_id = wikibase.id
    return wikibase_id


@pytest.mark.asyncio
async def test_update_missing_sparql_urls(
    wikibase_with_manifest, mocker
):  # pylint: disable=redefined-outer-name
    """Test update_missing_sparql_urls"""

    with open(f"{DATA_DIRECTORY}/manifest.json", mode="rb") as data:
        mocker.patch("requests.get", side_effect=[MockResponse("", 200, data.read())])

    before_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase_with_manifest}
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "id"],
        expected_value=str(wikibase_with_manifest),
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "scriptPath"],
        expected_value="/mockwiki",
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value=None,
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "sparqlFrontendUrl"],
        expected_value=None,
    )

    result = await update_missing_sparql_urls()
    assert result == 1

    after_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase_with_manifest}
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "id"],
        expected_value=str(wikibase_with_manifest),
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value="https://mock-wikibase.com/query/sparql",
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "sparqlFrontendUrl"],
        expected_value="https://mock-wikibase.com/query",
    )
