from datetime import datetime
from fetch_data.log_data.fetch_log_data import get_log_list_from_url


def test_get_log_list_from_url_empty(mocker):
    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        return_value={"query": {"logevents": []}},
    )
    assert get_log_list_from_url("test.url") == []


def test_get_log_list_from_url_single(mocker):
    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        return_value={
            "query": {
                "logevents": [
                    {
                        "logid": 1,
                        "timestamp": "2024-01-01T12:04:15Z",
                        "type": "create",
                        "action": "create",
                        "title": "Property:P17",
                    }
                ]
            }
        },
    )
    results = get_log_list_from_url("test.url")
    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].log_date == datetime(2024, 1, 1, 12, 4, 15)
    assert results[0].age() > 0
    assert results[0].user is None
    assert results[0].log_type.name == "PROPERTY_CREATE"
