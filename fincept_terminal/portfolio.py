"""Portfolio module: manage a simple portfolio of holdings."""

from fincept_terminal.config import get, set_value

PORTFOLIO_KEY = "portfolio"


def _load() -> dict:
    """Return the current portfolio dict {SYMBOL: quantity}."""
    return get(PORTFOLIO_KEY, {})


def _save(portfolio: dict) -> None:
    set_value(PORTFOLIO_KEY, portfolio)


def get_portfolio() -> dict:
    """Return a copy of the current portfolio."""
    return dict(_load())


def add_holding(symbol: str, quantity: float) -> bool:
    """Add *quantity* units of *symbol*.

    Returns True if the holding was added/updated, False if quantity <= 0.
    """
    if quantity <= 0:
        return False
    symbol = symbol.upper()
    portfolio = _load()
    portfolio[symbol] = portfolio.get(symbol, 0.0) + quantity
    _save(portfolio)
    return True


def remove_holding(symbol: str, quantity: float | None = None) -> bool:
    """Remove *quantity* units of *symbol*, or the entire position if quantity is None.

    Returns True on success, False if symbol not found or quantity invalid.
    """
    symbol = symbol.upper()
    portfolio = _load()
    if symbol not in portfolio:
        return False
    if quantity is None or quantity >= portfolio[symbol]:
        del portfolio[symbol]
    elif quantity <= 0:
        return False
    else:
        portfolio[symbol] -= quantity
    _save(portfolio)
    return True


def clear_portfolio() -> None:
    """Remove all holdings."""
    _save({})


def total_value(prices: dict) -> float:
    """Compute total portfolio value given a {SYMBOL: price} mapping."""
    portfolio = _load()
    return sum(portfolio.get(sym, 0.0) * price for sym, price in prices.items())
