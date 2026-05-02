"""Tests for the aurora_forecast plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.aurora_forecast import AuroraForecastPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "aurora_forecast",
    "name": "Aurora Forecast",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to fetch aurora data.",
                "default": 300,
                "minimum": 180
            }
        },
        "required": []
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
[
    {
        "time_tag": "2026-05-01T12:00:00Z",
        "kp_index": 2.0,
        "observed": "estimated"
    },
    {
        "time_tag": "2026-05-01T12:15:00Z",
        "kp_index": 3.67,
        "observed": "estimated"
    }
]
""")


@pytest.fixture
def plugin():
    return AuroraForecastPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = AuroraForecastPlugin(MANIFEST)
    p.config = json.loads("""
{}
""")
    return p


class TestAuroraForecastPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "aurora_forecast"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.aurora_forecast.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "kp_index" in result.data, "missing variable: kp_index"
        assert "activity" in result.data, "missing variable: activity"
        assert "aurora_visible" in result.data, "missing variable: aurora_visible"

    @patch("plugins.aurora_forecast.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.aurora_forecast.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

