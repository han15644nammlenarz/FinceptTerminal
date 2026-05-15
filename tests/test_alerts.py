"""Tests for fincept_terminal.alerts."""

import pytest
from fincept_terminal import alerts as al
from fincept_terminal.config import set_value


@pytest.fixture(autouse=True)
def reset_alerts():
    """Wipe alerts before every test."""
    set_value(al.ALERTS_KEY, {})
    yield
    set_value(al.ALERTS_KEY, {})


def test_get_alerts_empty():
    assert al.get_alerts() == {}


def test_add_alert_returns_true():
    assert al.add_alert("AAPL", 200.0) is True


def test_add_alert_normalises_case():
    al.add_alert("aapl", 150.0, "below")
    assert "AAPL" in al.get_alerts()


def test_add_duplicate_returns_false():
    al.add_alert("TSLA", 300.0, "above")
    assert al.add_alert("TSLA", 300.0, "above") is False


def test_add_different_direction_allowed():
    al.add_alert("TSLA", 300.0, "above")
    assert al.add_alert("TSLA", 300.0, "below") is True
    assert len(al.get_alerts()["TSLA"]) == 2


def test_add_multiple_alerts_same_symbol():
    al.add_alert("MSFT", 400.0)
    al.add_alert("MSFT", 350.0, "below")
    assert len(al.get_alerts()["MSFT"]) == 2


def test_invalid_direction_raises():
    with pytest.raises(ValueError):
        al.add_alert("GOOG", 100.0, "sideways")


def test_remove_alert_returns_true():
    al.add_alert("AMZN", 180.0)
    assert al.remove_alert("AMZN", 180.0) is True


def test_remove_alert_cleans_up_symbol_key():
    al.add_alert("AMZN", 180.0)
    al.remove_alert("AMZN", 180.0)
    assert "AMZN" not in al.get_alerts()


def test_remove_nonexistent_alert_returns_false():
    assert al.remove_alert("NFLX", 500.0) is False


def test_clear_single_symbol():
    al.add_alert("IBM", 140.0)
    al.add_alert("ORCL", 120.0)
    al.clear_alerts("IBM")
    result = al.get_alerts()
    assert "IBM" not in result
    assert "ORCL" in result


def test_clear_all_alerts():
    al.add_alert("IBM", 140.0)
    al.add_alert("ORCL", 120.0)
    al.clear_alerts()
    assert al.get_alerts() == {}
