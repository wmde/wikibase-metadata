"""Assert Aggregate Software Version"""

from datetime import datetime
from typing import Optional
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_property_value,
    SOFTWARE_VERSION_DATETIME_FORMAT,
)


def assert_software_version_aggregate(
    returned: dict,
    expected_software_name: str,
    expected_wikibase_count: int,
    expected_version_string: str,
    expected_version_semver: tuple[Optional[int], Optional[int], Optional[int]],
    expected_version_date: Optional[datetime],
    expected_version_hash: Optional[str],
):
    """Assert Aggregate Software Version"""

    assert_property_value(returned, "softwareName", expected_software_name)

    assert_property_value(returned, "softwareName", expected_software_name)
    assert_property_value(returned, "wikibaseCount", expected_wikibase_count)
    assert_layered_property_count(returned, ["versions"], 1)

    assert_layered_property_value(
        returned, ["versions", 0, "version"], expected_version_string
    )
    assert_layered_property_value(
        returned,
        ["versions", 0, "versionDate"],
        (
            expected_version_date.strftime(SOFTWARE_VERSION_DATETIME_FORMAT)
            if expected_version_date is not None
            else None
        ),
    )
    assert_layered_property_value(
        returned, ["versions", 0, "versionHash"], expected_version_hash
    )
    assert_layered_property_value(
        returned, ["versions", 0, "wikibaseCount"], expected_wikibase_count
    )

    assert_semver_aggregate(returned, expected_wikibase_count, expected_version_semver)


def assert_semver_aggregate(
    returned: dict,
    expected_wikibase_count: int,
    expected_version_semver: tuple[Optional[int], Optional[int], Optional[int]],
):
    """Assert SemVer Aggregate"""

    expected_version_major, expected_version_minor, expected_version_patch = (
        expected_version_semver
    )

    assert_layered_property_count(returned, ["majorVersions"], 1)
    assert_layered_property_value(
        returned,
        ["majorVersions", 0, "version"],
        str(expected_version_major) if expected_version_major is not None else None,
    )
    assert_layered_property_value(
        returned, ["majorVersions", 0, "wikibaseCount"], expected_wikibase_count
    )
    if expected_version_major is None:
        assert_layered_property_value(
            returned, ["majorVersions", 0, "minorVersions"], None
        )
    else:
        assert_layered_property_count(
            returned, ["majorVersions", 0, "minorVersions"], 1
        )
        assert_layered_property_value(
            returned,
            ["majorVersions", 0, "minorVersions", 0, "version"],
            f"{expected_version_major}.{expected_version_minor}",
        )
        assert_layered_property_value(
            returned,
            ["majorVersions", 0, "minorVersions", 0, "wikibaseCount"],
            expected_wikibase_count,
        )
        assert_layered_property_count(
            returned, ["majorVersions", 0, "minorVersions", 0, "patchVersions"], 1
        )
        assert_layered_property_value(
            returned,
            ["majorVersions", 0, "minorVersions", 0, "patchVersions", 0, "version"],
            (
                f"{expected_version_major}.{expected_version_minor}.{expected_version_patch}"
                if expected_version_patch is not None
                else f"{expected_version_major}.{expected_version_minor}"
            ),
        )
        assert_layered_property_value(
            returned,
            [
                "majorVersions",
                0,
                "minorVersions",
                0,
                "patchVersions",
                0,
                "wikibaseCount",
            ],
            expected_wikibase_count,
        )
