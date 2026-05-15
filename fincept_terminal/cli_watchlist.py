"""Click CLI commands for watchlist management."""

import click

from fincept_terminal.watchlist_handler import (
    show_watchlist,
    handle_add,
    handle_remove,
    handle_clear,
)


@click.group(name="watchlist")
def watchlist_group():
    """Manage your asset watchlist."""


@watchlist_group.command(name="show")
def cmd_show():
    """Display all symbols in the watchlist."""
    show_watchlist()


@watchlist_group.command(name="add")
@click.argument("symbol")
def cmd_add(symbol: str):
    """Add SYMBOL to the watchlist."""
    handle_add(symbol)


@watchlist_group.command(name="remove")
@click.argument("symbol")
def cmd_remove(symbol: str):
    """Remove SYMBOL from the watchlist."""
    handle_remove(symbol)


@watchlist_group.command(name="clear")
def cmd_clear():
    """Clear all symbols from the watchlist."""
    handle_clear()
