# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import asyncio
from typing import List

import pytest
import requests
from tests.utils import MockResponse


from fetch_data.utils.fetch_data_from_api import fetch_api_data, APIError


@pytest.mark.asyncio
async def test_fetch_api_data_success(monkeypatch):
    """Returns parsed JSON on first try."""

    def fake_get(url, timeout, headers):
        assert url == "http://example.com/api"
        assert timeout == 300
        return MockResponse(url, 200, '{"ok": true, "value": 42}')

    monkeypatch.setattr(requests, "get", fake_get)

    data = await fetch_api_data(
        "http://example.com/api", initial_wait=0.01, max_retries=0
    )
    assert data == {"ok": True, "value": 42}


@pytest.mark.asyncio
async def test_fetch_api_data_retries_then_succeeds(monkeypatch):
    """Retries on exceptions, applies exponential backoff, then succeeds."""

    calls: List[str] = []
    sleep_calls: List[float] = []

    async def fake_sleep(delay):
        sleep_calls.append(delay)

    # First two attempts raise, third succeeds
    side_effects = [
        requests.Timeout("timeout"),
        requests.ConnectionError("conn error"),
        MockResponse("https://example.com", 200, '{"ok": true, "value": 42}'),
    ]

    def fake_get(url, timeout, headers):  # pylint: disable=unused-argument
        calls.append(url)
        effect = side_effects.pop(0)
        if isinstance(effect, Exception):
            raise effect
        return effect

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    data = await fetch_api_data(
        "http://example.com/api",
        initial_wait=0.01,
        max_retries=4,
        multiplier=2.0,
    )

    assert data == {"ok": True, "value": 42}
    # Two failures -> two sleeps, with exponential wait
    assert sleep_calls == [0.01, 0.02]
    # Three total calls made
    assert len(calls) == 3


@pytest.mark.asyncio
async def test_fetch_api_data_all_retries_fail(monkeypatch):
    """Raises the last exception after exhausting retries."""

    sleep_calls: List[float] = []

    async def fake_sleep(delay):
        sleep_calls.append(delay)

    def fake_get(url, timeout, headers):
        raise requests.RequestException("boom")

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    with pytest.raises(requests.RequestException):
        await fetch_api_data(
            "http://example.com/api",
            initial_wait=0.01,
            max_retries=2,
            multiplier=2.0,
        )

    # Slept once per failed retry attempt (not after the final attempt)
    assert sleep_calls == [0.01, 0.02]


@pytest.mark.asyncio
async def test_fetch_api_data_instant_fail_on_404(monkeypatch):
    """Tests that an API error 404 is handled as a failure without retries."""

    sleep_calls: List[float] = []

    async def fake_sleep(delay):
        sleep_calls.append(delay)

    def fake_get(url, timeout, headers):
        return MockResponse(url, 404)

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    with pytest.raises(APIError):
        await fetch_api_data("http://example.com/api")

    # did not sleep at all
    assert sleep_calls == []


@pytest.mark.asyncio
async def test_fetch_api_data_api_error_json_retries_then_raises(monkeypatch):
    """When API returns an error JSON, it retries and finally raises ValueError."""

    sleep_calls: List[float] = []

    async def fake_sleep(delay):
        sleep_calls.append(delay)

    def fake_get(url, timeout, headers):  # pylint: disable=unused-argument
        return MockResponse(url, 500)

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    with pytest.raises(APIError):
        await fetch_api_data(
            "http://example.com/api",
            initial_wait=0.01,
            max_retries=3,
            multiplier=2.0,
        )

    # Should retry up to max_retries times -> 3 sleeps
    assert sleep_calls == [0.01, 0.02, 0.04]
