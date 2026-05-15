"""Price alert management for FinceptTerminal."""

from fincept_terminal.config import get, set_value

ALERTS_KEY = "price_alerts"


def _load() -> dict:
    """Load alerts dict from config; keys are uppercased symbols."""
    return get(ALERTS_KEY, {})


def _save(alerts: dict) -> None:
    set_value(ALERTS_KEY, alerts)


def get_alerts() -> dict:
    """Return a copy of all price alerts."""
    return dict(_load())


def add_alert(symbol: str, price: float, direction: str = "above") -> bool:
    """Add a price alert for *symbol*.

    Parameters
    ----------
    symbol:    Ticker symbol (case-insensitive).
    price:     Target price that should trigger the alert.
    direction: ``'above'`` or ``'below'``.

    Returns ``True`` if the alert was added, ``False`` if an identical alert
    already exists.
    """
    if direction not in ("above", "below"):
        raise ValueError("direction must be 'above' or 'below'")

    symbol = symbol.upper().strip()
    alerts = _load()
    entry = {"price": float(price), "direction": direction}

    existing = alerts.get(symbol, [])
    if entry in existing:
        return False

    existing.append(entry)
    alerts[symbol] = existing
    _save(alerts)
    return True


def remove_alert(symbol: str, price: float, direction: str = "above") -> bool:
    """Remove a specific alert.  Returns ``True`` if it existed."""
    symbol = symbol.upper().strip()
    alerts = _load()
    entry = {"price": float(price), "direction": direction}

    existing = alerts.get(symbol, [])
    if entry not in existing:
        return False

    existing.remove(entry)
    if existing:
        alerts[symbol] = existing
    else:
        alerts.pop(symbol, None)
    _save(alerts)
    return True


def clear_alerts(symbol: str | None = None) -> None:
    """Clear alerts for one symbol, or all alerts when *symbol* is ``None``."""
    if symbol is None:
        _save({})
    else:
        alerts = _load()
        alerts.pop(symbol.upper().strip(), None)
        _save(alerts)
