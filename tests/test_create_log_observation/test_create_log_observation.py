from fetch_data.log_data.fetch_log_data import get_log_list_from_url


def test_get_log_list_from_url_empty(mocker):
    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        return_value={"query": {"logevents": []}},
    )
    assert get_log_list_from_url("test.url") == []
