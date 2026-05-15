"""Watchlist module for FinceptTerminal.

Provides functions to manage a user's stock/asset watchlist,
stored via the config system.
"""

from fincept_terminal.config import get, set_value

WATCHLIST_KEY = "watchlist"


def get_watchlist() -> list:
    """Return the current watchlist."""
    return get(WATCHLIST_KEY, default=[])


def add_symbol(symbol: str) -> bool:
    """Add a symbol to the watchlist.

    Returns True if added, False if already present.
    """
    symbol = symbol.upper().strip()
    watchlist = get_watchlist()
    if symbol in watchlist:
        return False
    watchlist.append(symbol)
    set_value(WATCHLIST_KEY, watchlist)
    return True


def remove_symbol(symbol: str) -> bool:
    """Remove a symbol from the watchlist.

    Returns True if removed, False if not found.
    """
    symbol = symbol.upper().strip()
    watchlist = get_watchlist()
    if symbol not in watchlist:
        return False
    watchlist.remove(symbol)
    set_value(WATCHLIST_KEY, watchlist)
    return True


def clear_watchlist() -> None:
    """Remove all symbols from the watchlist."""
    set_value(WATCHLIST_KEY, [])


def is_in_watchlist(symbol: str) -> bool:
    """Check whether a symbol is in the watchlist."""
    return symbol.upper().strip() in get_watchlist()


def watchlist_count() -> int:
    """Return the number of symbols currently in the watchlist."""
    return len(get_watchlist())
