# pylint: disable=missing-function-docstring


"""Tests for get_recent_changes_param_string"""

from fetch_data.api_data.recent_changes_data.fetch_recent_changes_data import (
    get_recent_changes_param_string,
)


def test_param_string_defaults_bots_false():
    expected = (
        "?action=query"
        "&format=json"
        "&list=recentchanges"
        "&formatversion=2"
        "&rcprop=user|userid|timestamp"
        "&rcshow=!bot"
    )
    assert get_recent_changes_param_string() == expected


def test_param_string_bots_true():
    expected = (
        "?action=query"
        "&format=json"
        "&list=recentchanges"
        "&formatversion=2"
        "&rcprop=user|userid|timestamp"
        "&rcshow=bot"
    )
    assert get_recent_changes_param_string(bots=True) == expected


def test_param_string_with_limit():
    expected = (
        "?action=query"
        "&format=json"
        "&list=recentchanges"
        "&formatversion=2"
        "&rcprop=user|userid|timestamp"
        "&rclimit=500"
        "&rcshow=!bot"
    )
    assert get_recent_changes_param_string(limit=500) == expected


def test_param_string_with_continue():
    cont = "2024-02-10T01:00:00Z|12345"
    expected = (
        "?action=query"
        "&format=json"
        "&list=recentchanges"
        "&formatversion=2"
        "&rcprop=user|userid|timestamp"
        "&rcshow=!bot"
        f"&rccontinue={cont}"
    )
    assert get_recent_changes_param_string(continue_from=cont) == expected


def test_param_string_all_params_bots_true():
    cont = "2024-02-04T12:00:00Z|54321"
    expected = (
        "?action=query"
        "&format=json"
        "&list=recentchanges"
        "&formatversion=2"
        "&rcprop=user|userid|timestamp"
        "&rclimit=50"
        "&rcshow=bot"
        f"&rccontinue={cont}"
    )
    assert (
        get_recent_changes_param_string(limit=50, continue_from=cont, bots=True)
        == expected
    )
