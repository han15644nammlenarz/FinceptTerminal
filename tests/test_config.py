"""Tests for configuration management in FinceptTerminal."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

import fincept_terminal.config as cfg
from fincept_terminal.config_handler import (
    add_to_watchlist,
    remove_from_watchlist,
    set_api_key,
    reset_config,
)


@pytest.fixture(autouse=True)
def tmp_config(tmp_path, monkeypatch):
    """Redirect config paths to a temporary directory for each test."""
    monkeypatch.setattr(cfg, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(cfg, "CONFIG_FILE", tmp_path / "config.json")
    yield tmp_path


def test_load_config_creates_default(tmp_config):
    config = cfg.load_config()
    assert config["theme"] == "dark"
    assert (tmp_config / "config.json").exists()


def test_save_and_load_roundtrip(tmp_config):
    data = cfg.DEFAULT_CONFIG.copy()
    data["theme"] = "light"
    cfg.save_config(data)
    loaded = cfg.load_config()
    assert loaded["theme"] == "light"


def test_get_returns_default_for_missing_key(tmp_config):
    value = cfg.get("nonexistent_key", "fallback")
    assert value == "fallback"


def test_set_value_persists(tmp_config):
    cfg.set_value("refresh_interval", 120)
    assert cfg.get("refresh_interval") == 120


def test_add_to_watchlist(tmp_config):
    add_to_watchlist("aapl")
    assert "AAPL" in cfg.get("watchlist")


def test_add_duplicate_watchlist(tmp_config, capsys):
    add_to_watchlist("TSLA")
    add_to_watchlist("TSLA")
    captured = capsys.readouterr()
    assert "already in the watchlist" in captured.out
    assert cfg.get("watchlist").count("TSLA") == 1


def test_remove_from_watchlist(tmp_config):
    add_to_watchlist("MSFT")
    remove_from_watchlist("MSFT")
    assert "MSFT" not in cfg.get("watchlist")


def test_remove_nonexistent_watchlist(tmp_config, capsys):
    remove_from_watchlist("GOOG")
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_set_api_key(tmp_config):
    set_api_key("AlphaVantage", "secret123")
    api_keys = cfg.get("api_keys")
    assert api_keys.get("alphavantage") == "secret123"


def test_reset_config(tmp_config):
    cfg.set_value("theme", "custom")
    reset_config()
    assert cfg.get("theme") == cfg.DEFAULT_CONFIG["theme"]
