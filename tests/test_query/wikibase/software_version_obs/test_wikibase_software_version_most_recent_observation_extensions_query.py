"""Test Wikibase Most Recent Software Version Installed Extensions Observation Query"""

from datetime import datetime
import pytest
from tests.test_query.wikibase.software_version_obs.assert_software_version import (
    assert_software_version,
)
from tests.test_query.wikibase.software_version_obs.software_version_fragment import (
    WIKIBASE_SOFTWARE_VERSION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value


WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_EXTENSIONS_QUERY = (
    """
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

"""
    + WIKIBASE_SOFTWARE_VERSION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["software-version-success"], scope="session")
@pytest.mark.query
@pytest.mark.version
async def test_wikibase_software_version_most_recent_observation_extensions_query():
    """Test Wikibase Most Recent Software Version Installed Extensions Observation Query"""

    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_EXTENSIONS_QUERY,
        variable_values={"wikibaseId": 1},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "softwareVersionObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["softwareVersionObservations"]
    most_recent = result_wikibase["softwareVersionObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", "1")
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)

    assert_layered_property_count(most_recent, ["installedExtensions"], 11)
    for index, (
        expected_id,
        expected_name,
        expected_version,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("9", "Babel", "1.11.1", None, None),
            (
                "16",
                "Google Analytics Integration",
                "3.0.1",
                datetime(2019, 8, 6, 9, 12),
                "6441403",
            ),
            (
                "10",
                "LabeledSectionTransclusion",
                "f621799",
                datetime(2020, 1, 29, 14, 52),
                "f621799",
            ),
            (
                "19",
                "Miraheze Magic",
                "e742444",
                datetime(2024, 10, 17, 15, 21),
                "e742444",
            ),
            ("17", "ProofreadPage", "cb0a218", datetime(2019, 9, 30, 9, 20), "cb0a218"),
            ("11", "Scribunto", None, None, None),
            (
                "18",
                "UniversalLanguageSelector",
                "2020-01-23",
                datetime(2020, 3, 3, 13, 38),
                "61f1a98",
            ),
            (
                "12",
                "WikibaseClient",
                "dbbcdd8",
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
            ("13", "WikibaseLib", "dbbcdd8", datetime(2019, 12, 10, 12, 52), "dbbcdd8"),
            (
                "14",
                "WikibaseRepository",
                "dbbcdd8",
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
            (
                "15",
                "WikibaseView",
                "dbbcdd8",
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
        ]
    ):
        assert_software_version(
            most_recent["installedExtensions"][index],
            expected_id,
            expected_name,
            expected_version,
            expected_version_date,
            expected_version_hash,
        )
