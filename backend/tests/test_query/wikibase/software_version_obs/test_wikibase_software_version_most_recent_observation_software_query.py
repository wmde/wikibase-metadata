"""Test Wikibase Most Recent Software Version Installed Software Observation Query"""

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
from tests.test_query.wikibase.software_version_obs.assert_software_version import (
    assert_software_version,
)
from tests.test_query.wikibase.software_version_obs.software_version_fragment import (
    WIKIBASE_SOFTWARE_VERSION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value

WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_SOFTWARE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    softwareVersionObservations {
      mostRecent {
        id
        observationDate
        returnedData
        installedSoftware {
          ...WikibaseSoftwareVersionFragment
        }
      }
    }
  }
}

""" + WIKIBASE_SOFTWARE_VERSION_FRAGMENT


@pytest.fixture
async def wikibase_with_software_observation(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with software version observation containing 5 software entries"""
    async with get_async_session() as session:
        software_data = [
            ("ICU", "60.2", None, None),
            ("Lua", "5.1.5", None, None),
            ("MediaWiki", "1.39.8", None, "fbca402"),
            ("MySQL", "1.35.8", datetime(2022, 12, 13, 5, 50), "e43140f"),
            ("PHP", "7.2.24-0ubuntu0.18.04.3 (fpm-fcgi)", None, None),
        ]

        software_models = {}
        for name, _, _, _ in software_data:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.SOFTWARE,
                software_name=name,
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)
            software_models[name] = software

        wikibase = WikibaseModel(
            wikibase_name="Software Version Software Test Wikibase",
            base_url="https://software-version-software-example.com",
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

        for name, version, version_date, version_hash in software_data:
            sv = WikibaseSoftwareVersionModel(
                software=software_models[name],
                version=version,
                version_date=version_date,
                version_hash=version_hash,
            )
            sv.wikibase_software_version_observation_id = obs.id
            session.add(sv)
            await session.flush()
            await session.refresh(sv)

        wikibase_id = wikibase.id
        observation_id = str(obs.id)
    return wikibase_id, observation_id


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
async def test_wikibase_software_version_most_recent_observation_software_query(
    wikibase_with_software_observation,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase Most Recent Software Version Installed Software Observation Query"""

    wikibase_id, observation_id = wikibase_with_software_observation

    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_SOFTWARE_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "softwareVersionObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["softwareVersionObservations"]
    most_recent = result_wikibase["softwareVersionObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", observation_id)
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)

    assert_layered_property_count(most_recent, ["installedSoftware"], 5)
    for index, (
        name,
        expected_version,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("ICU", "60.2", None, None),
            ("Lua", "5.1.5", None, None),
            ("MediaWiki", "1.39.8", None, "fbca402"),
            ("MySQL", "1.35.8", datetime(2022, 12, 13, 5, 50), "e43140f"),
            ("PHP", "7.2.24-0ubuntu0.18.04.3 (fpm-fcgi)", None, None),
        ]
    ):
        assert_software_version(
            most_recent["installedSoftware"][index],
            name,
            expected_version,
            expected_version_date,
            expected_version_hash,
        )
