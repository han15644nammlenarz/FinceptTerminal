"""Tests for fincept_terminal.watchlist_handler module."""

import pytest
from click.testing import CliRunner

from fincept_terminal import config as cfg
from fincept_terminal import watchlist as wl
from fincept_terminal.cli_watchlist import watchlist_group


@pytest.fixture(autouse=True)
def reset_watchlist(tmp_path, monkeypatch):
    config_file = tmp_path / "settings.json"
    monkeypatch.setattr(cfg, "CONFIG_PATH", str(config_file))
    cfg.save_config({})
    yield


@pytest.fixture
def runner():
    return CliRunner()


def test_show_empty(runner):
    result = runner.invoke(watchlist_group, ["show"])
    assert result.exit_code == 0
    assert "empty" in result.output.lower()


def test_add_via_cli(runner):
    result = runner.invoke(watchlist_group, ["add", "AAPL"])
    assert result.exit_code == 0
    assert "added" in result.output.lower()
    assert wl.is_in_watchlist("AAPL")


def test_add_duplicate_via_cli(runner):
    runner.invoke(watchlist_group, ["add", "AAPL"])
    result = runner.invoke(watchlist_group, ["add", "AAPL"])
    assert "already" in result.output.lower()


def test_remove_via_cli(runner):
    wl.add_symbol("TSLA")
    result = runner.invoke(watchlist_group, ["remove", "TSLA"])
    assert result.exit_code == 0
    assert "removed" in result.output.lower()
    assert not wl.is_in_watchlist("TSLA")


def test_remove_missing_via_cli(runner):
    result = runner.invoke(watchlist_group, ["remove", "FAKE"])
    assert "not found" in result.output.lower()


def test_clear_via_cli(runner):
    wl.add_symbol("GOOG")
    result = runner.invoke(watchlist_group, ["clear"])
    assert result.exit_code == 0
    assert "cleared" in result.output.lower()
    assert wl.watchlist_count() == 0


def test_show_with_symbols(runner):
    wl.add_symbol("AMZN")
    wl.add_symbol("NVDA")
    result = runner.invoke(watchlist_group, ["show"])
    assert "AMZN" in result.output
    assert "NVDA" in result.output
