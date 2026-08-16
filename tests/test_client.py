"""Unit tests for PepkioClient with mocked HTTP."""

from __future__ import annotations

import httpx
import pytest

from pepkio_dmp_in_a_flash.client import PepkioClient
from pepkio_dmp_in_a_flash.config import resolve_api_key, resolve_base_url
from pepkio_dmp_in_a_flash.exceptions import PepkioAPIError


def test_resolve_base_url_default():
    assert resolve_base_url() == "https://tools.pepkio.com"
    assert resolve_base_url("https://tools.localtest.me/") == "https://tools.localtest.me"


def test_resolve_api_key(monkeypatch):
    monkeypatch.setenv("PEPKIO_API_KEY", "prod_key_123")
    monkeypatch.setenv("LOCAL_PEPKIO_API_KEY", "local_key_123")

    assert resolve_api_key(base_url="https://tools.pepkio.com") == "prod_key_123"
    assert resolve_api_key(base_url="https://tools.localtest.me") == "local_key_123"
    assert resolve_api_key("override_key") == "override_key"


def test_client_missing_api_key(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_PEPKIO_API_KEY", raising=False)
    client = PepkioClient(api_key=None, base_url="https://tools.pepkio.com")
    with pytest.raises(ValueError, match="API key required"):
        client.run({"action": "load_preset", "scenarioId": "human-wgs-clinical"})


def test_get_manifest_success(mock_manifest):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/dmp-in-a-flash/manifest"
        return httpx.Response(200, json=mock_manifest)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(base_url=client.base_url, transport=transport)
        manifest = client.get_manifest()
        assert manifest["tool_id"] == "dmp-in-a-flash"
        assert len(client.list_examples()) == 2
        assert "generate_mouse_rnaseq" in client.list_examples()

        ex_input = client.get_example_input("generate_mouse_rnaseq")
        assert ex_input["action"] == "generate"
        assert ex_input["funder"] == "nih-2026"


def test_run_success(mock_run_response):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/dmp-in-a-flash/run"
        assert request.headers.get("Authorization") == "Bearer test_key"
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        result = client.run(
            {"action": "generate", "funder": "nih-2026"},
            label="test-run",
        )
        assert result.status == "completed"
        assert result.run_id == "run_dmp123"
        assert "text" in result.result


def test_get_run_success(mock_run_response):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/run_dmp123"
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        result = client.get_run("run_dmp123")
        assert result.status == "completed"
        assert result.run_id == "run_dmp123"


def test_api_error_response():
    def handle_request(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={"error": {"message": "Invalid funder", "code": "INVALID_INPUT"}},
        )

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        with pytest.raises(PepkioAPIError) as exc_info:
            client.run({"action": "generate", "funder": "invalid_funder"})
        assert exc_info.value.status_code == 400
        assert "Invalid funder" in str(exc_info.value)
