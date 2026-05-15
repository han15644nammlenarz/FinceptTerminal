"""Portfolio handler: Rich-formatted display and CLI interaction helpers."""

from rich.console import Console
from rich.table import Table

from fincept_terminal.portfolio import (
    get_portfolio,
    add_holding,
    remove_holding,
    clear_portfolio,
)

console = Console()


def show_portfolio() -> None:
    """Print the current portfolio as a Rich table."""
    portfolio = get_portfolio()
    if not portfolio:
        console.print("[yellow]Portfolio is empty.[/yellow]")
        return

    table = Table(title="Portfolio", show_header=True, header_style="bold cyan")
    table.add_column("Symbol", style="bold")
    table.add_column("Quantity", justify="right")

    for symbol, qty in sorted(portfolio.items()):
        table.add_row(symbol, f"{qty:,.4f}")

    console.print(table)


def handle_add(symbol: str, quantity: float) -> None:
    if add_holding(symbol, quantity):
        console.print(f"[green]Added {quantity} × {symbol.upper()} to portfolio.[/green]")
    else:
        console.print("[red]Quantity must be greater than zero.[/red]")


def handle_remove(symbol: str, quantity: float | None = None) -> None:
    if remove_holding(symbol, quantity):
        msg = f"[green]Removed {symbol.upper()}"
        if quantity is not None:
            msg += f" ({quantity} units)"
        console.print(msg + " from portfolio.[/green]")
    else:
        console.print(f"[red]{symbol.upper()} not found in portfolio or invalid quantity.[/red]")


def handle_clear() -> None:
    clear_portfolio()
    console.print("[green]Portfolio cleared.[/green]")
