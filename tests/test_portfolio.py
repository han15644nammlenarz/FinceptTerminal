"""Tests for the portfolio module."""

import pytest

from fincept_terminal import portfolio as pf


@pytest.fixture(autouse=True)
def reset_portfolio(tmp_path, monkeypatch):
    """Isolate config to a temp directory and clear portfolio before each test."""
    import fincept_terminal.config as cfg

    monkeypatch.setattr(cfg, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(cfg, "CONFIG_FILE", tmp_path / "config.json")
    # Reset in-memory cache
    cfg._config_cache = None  # noqa: SLF001
    pf.clear_portfolio()
    yield
    pf.clear_portfolio()


def test_get_portfolio_empty():
    assert pf.get_portfolio() == {}


def test_add_holding():
    result = pf.add_holding("aapl", 10)
    assert result is True
    assert pf.get_portfolio() == {"AAPL": 10.0}


def test_add_holding_normalises_case():
    pf.add_holding("tsla", 5)
    assert "TSLA" in pf.get_portfolio()


def test_add_holding_accumulates():
    pf.add_holding("MSFT", 3)
    pf.add_holding("msft", 7)
    assert pf.get_portfolio()["MSFT"] == pytest.approx(10.0)


def test_add_holding_zero_returns_false():
    assert pf.add_holding("GOOG", 0) is False
    assert "GOOG" not in pf.get_portfolio()


def test_add_holding_negative_returns_false():
    assert pf.add_holding("GOOG", -5) is False


def test_remove_holding_full():
    pf.add_holding("AMZN", 4)
    result = pf.remove_holding("AMZN")
    assert result is True
    assert "AMZN" not in pf.get_portfolio()


def test_remove_holding_partial():
    pf.add_holding("NVDA", 10)
    pf.remove_holding("NVDA", 3)
    assert pf.get_portfolio()["NVDA"] == pytest.approx(7.0)


def test_remove_holding_not_found():
    assert pf.remove_holding("UNKNOWN") is False


def test_remove_holding_invalid_quantity():
    pf.add_holding("META", 5)
    assert pf.remove_holding("META", -1) is False


def test_clear_portfolio():
    pf.add_holding("SPY", 100)
    pf.clear_portfolio()
    assert pf.get_portfolio() == {}


def test_total_value():
    pf.add_holding("AAPL", 2)
    pf.add_holding("MSFT", 3)
    prices = {"AAPL": 150.0, "MSFT": 300.0}
    assert pf.total_value(prices) == pytest.approx(2 * 150.0 + 3 * 300.0)
