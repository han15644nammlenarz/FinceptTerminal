"""Tests for fincept_terminal.watchlist module."""

import pytest

from fincept_terminal import config as cfg
from fincept_terminal import watchlist as wl


@pytest.fixture(autouse=True)
def reset_watchlist(tmp_path, monkeypatch):
    """Redirect config to a temp directory and reset watchlist before each test."""
    config_file = tmp_path / "settings.json"
    monkeypatch.setattr(cfg, "CONFIG_PATH", str(config_file))
    cfg.save_config({})
    yield


def test_get_watchlist_empty():
    assert wl.get_watchlist() == []


def test_add_symbol():
    result = wl.add_symbol("AAPL")
    assert result is True
    assert "AAPL" in wl.get_watchlist()


def test_add_symbol_normalises_case():
    wl.add_symbol("msft")
    assert "MSFT" in wl.get_watchlist()


def test_add_duplicate_returns_false():
    wl.add_symbol("TSLA")
    result = wl.add_symbol("TSLA")
    assert result is False
    assert wl.get_watchlist().count("TSLA") == 1


def test_remove_symbol():
    wl.add_symbol("GOOG")
    result = wl.remove_symbol("GOOG")
    assert result is True
    assert "GOOG" not in wl.get_watchlist()


def test_remove_missing_symbol_returns_false():
    result = wl.remove_symbol("NOPE")
    assert result is False


def test_clear_watchlist():
    wl.add_symbol("AMZN")
    wl.add_symbol("NVDA")
    wl.clear_watchlist()
    assert wl.get_watchlist() == []


def test_is_in_watchlist():
    wl.add_symbol("META")
    assert wl.is_in_watchlist("META") is True
    assert wl.is_in_watchlist("meta") is True
    assert wl.is_in_watchlist("AAPL") is False


def test_watchlist_count():
    assert wl.watchlist_count() == 0
    wl.add_symbol("A")
    wl.add_symbol("B")
    assert wl.watchlist_count() == 2
