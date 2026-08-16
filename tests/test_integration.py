"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv

from pepkio_dmp_in_a_flash.client import PepkioClient

load_dotenv()

ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    probe_timeout = 1.0 if "localtest.me" in base_url else 10.0
    try:
        with PepkioClient(api_key=api_key, base_url=base_url, timeout=probe_timeout) as client:
            client.get_manifest()
    except Exception as exc:
        pytest.skip(f"Environment {env_name} ({base_url}) unreachable: {exc}")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "dmp-in-a-flash"
    names = live_client.list_examples()
    assert "generate_mouse_rnaseq" in names


def test_run_generate_mouse_rnaseq_example(live_client: PepkioClient):
    inp = live_client.get_example_input("generate_mouse_rnaseq")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert "text" in result.result


def test_run_load_human_wgs_example(live_client: PepkioClient):
    inp = live_client.get_example_input("load_human_wgs")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert "intake" in result.result
