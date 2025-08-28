"""Test create_software_version_observation"""

from fetch_data.api_data.time_to_first_value.get_deleted_revisions_data import (
    get_del_rev_param_string,
    parse_del_rev_timestamp,
)
from fetch_data.api_data.time_to_first_value.get_revisions_data import (
    get_revision_param_string,
    parse_revision_timestamp,
)

DATA_DIRECTORY = "tests/test_create_observation/time_to_first_value/data"

FETCH_TTFV_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchTimeToFirstValueData(wikibaseId: $wikibaseId)
}"""


def test_get_revision_param_string_no_titles():
    """Test Param Strings"""

    try:
        get_revision_param_string(titles=[])
        assert False
    except ValueError:
        assert True


def test_get_revision_param_string_no_prop():
    """Test Param Strings"""

    assert (
        get_revision_param_string(titles=["T1"])
        == "?action=query&format=json&prop=revisions&titles=T1&rvdir=newer&rvlimit=1"
    )


def test_parse_revision_timestamp_empty():
    """Test Empty Returned"""

    try:
        parse_revision_timestamp({})
        assert False
    except KeyError:
        assert True


def test_get_del_rev_param_string_no_titles():
    """Test Param Strings"""

    try:
        get_del_rev_param_string(titles=[])
        assert False
    except ValueError:
        assert True


def test_get_del_rev_param_string_no_prop():
    """Test Param Strings"""

    assert (
        get_del_rev_param_string(titles=["T1"])
        == "?action=query&format=json&prop=deletedrevisions&titles=T1&drvdir=newer&drvlimit=1"
    )


def test_parse_del_rev_timestamp_empty():
    """Test Empty Returned"""

    try:
        parse_del_rev_timestamp({})
        assert False
    except KeyError:
        assert True
