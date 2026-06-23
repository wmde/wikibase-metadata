"""Test Wikibase Most Recent Software Version Installed Extensions Observation Query"""

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

WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_EXTENSIONS_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    softwareVersionObservations {
      mostRecent {
        id
        observationDate
        returnedData
        installedExtensions {
          ...WikibaseSoftwareVersionFragment
        }
      }
    }
  }
}

""" + WIKIBASE_SOFTWARE_VERSION_FRAGMENT


@pytest.fixture
async def wikibase_with_extensions_observation(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with software version observation containing extensions"""
    async with get_async_session() as session:
        extensions = [
            ("Babel", "1.11.1", None, None),
            (
                "Google Analytics Integration",
                "3.0.1",
                datetime(2019, 8, 6, 9, 12),
                "6441403",
            ),
            (
                "LabeledSectionTransclusion",
                "f621799",
                datetime(2020, 1, 29, 14, 52),
                "f621799",
            ),
            ("Miraheze Magic", "e742444", datetime(2024, 10, 17, 15, 21), "e742444"),
            ("ProofreadPage", "cb0a218", datetime(2019, 9, 30, 9, 20), "cb0a218"),
            ("Scribunto", None, None, None),
            (
                "UniversalLanguageSelector",
                "2020-01-23",
                datetime(2020, 3, 3, 13, 38),
                "61f1a98",
            ),
            ("WikibaseClient", "dbbcdd8", datetime(2019, 12, 10, 12, 52), "dbbcdd8"),
            ("WikibaseLib", "dbbcdd8", datetime(2019, 12, 10, 12, 52), "dbbcdd8"),
            (
                "WikibaseRepository",
                "dbbcdd8",
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
            ("WikibaseView", "dbbcdd8", datetime(2019, 12, 10, 12, 52), "dbbcdd8"),
        ]
        ext_software = {}
        for name, _, _, _ in extensions:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.EXTENSION,
                software_name=name,
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)
            ext_software[name] = software

        wikibase = WikibaseModel(
            wikibase_name="Extensions Test Wikibase",
            base_url="https://extensions-test-example.com",
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

        ext_ids = {}
        for name, version, version_date, version_hash in extensions:
            sv = WikibaseSoftwareVersionModel(
                software=ext_software[name],
                version=version,
                version_date=version_date,
                version_hash=version_hash,
            )
            sv.wikibase_software_version_observation_id = obs.id
            session.add(sv)
            await session.flush()
            await session.refresh(sv)
            ext_ids[name] = str(sv.id)

        wikibase_id = wikibase.id
        observation_id = str(obs.id)
    return wikibase_id, observation_id, ext_ids


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
async def test_wikibase_software_version_most_recent_observation_extensions_query(
    wikibase_with_extensions_observation,
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test Wikibase Most Recent Software Version Installed Extensions Observation Query"""

    wikibase_id, observation_id, ext_ids = wikibase_with_extensions_observation

    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_EXTENSIONS_QUERY,
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

    assert_layered_property_count(most_recent, ["installedExtensions"], 11)
    for index, (
        name,
        expected_version,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("Babel", "1.11.1", None, None),
            (
                "Google Analytics Integration",
                "3.0.1",
                datetime(2019, 8, 6, 9, 12),
                "6441403",
            ),
            (
                "LabeledSectionTransclusion",
                "f621799",
                datetime(2020, 1, 29, 14, 52),
                "f621799",
            ),
            ("Miraheze Magic", "e742444", datetime(2024, 10, 17, 15, 21), "e742444"),
            ("ProofreadPage", "cb0a218", datetime(2019, 9, 30, 9, 20), "cb0a218"),
            ("Scribunto", None, None, None),
            (
                "UniversalLanguageSelector",
                "2020-01-23",
                datetime(2020, 3, 3, 13, 38),
                "61f1a98",
            ),
            ("WikibaseClient", "dbbcdd8", datetime(2019, 12, 10, 12, 52), "dbbcdd8"),
            ("WikibaseLib", "dbbcdd8", datetime(2019, 12, 10, 12, 52), "dbbcdd8"),
            (
                "WikibaseRepository",
                "dbbcdd8",
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
            ("WikibaseView", "dbbcdd8", datetime(2019, 12, 10, 12, 52), "dbbcdd8"),
        ]
    ):
        assert_software_version(
            most_recent["installedExtensions"][index],
            ext_ids[name],
            name,
            expected_version,
            expected_version_date,
            expected_version_hash,
        )
