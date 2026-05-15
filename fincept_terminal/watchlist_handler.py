"""CLI handler for watchlist commands in FinceptTerminal."""

from rich.console import Console
from rich.table import Table

from fincept_terminal import watchlist as wl

console = Console()


def show_watchlist() -> None:
    """Display the current watchlist in a formatted table."""
    symbols = wl.get_watchlist()
    if not symbols:
        console.print("[yellow]Your watchlist is empty.[/yellow]")
        return

    table = Table(title="Watchlist", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Symbol", style="bold green")

    for idx, symbol in enumerate(symbols, start=1):
        table.add_row(str(idx), symbol)

    console.print(table)


def handle_add(symbol: str) -> None:
    """Handle adding a symbol to the watchlist."""
    if not symbol:
        console.print("[red]Please provide a symbol to add.[/red]")
        return
    added = wl.add_symbol(symbol)
    if added:
        console.print(f"[green]'{symbol.upper()}' added to watchlist.[/green]")
    else:
        console.print(f"[yellow]'{symbol.upper()}' is already in your watchlist.[/yellow]")


def handle_remove(symbol: str) -> None:
    """Handle removing a symbol from the watchlist."""
    if not symbol:
        console.print("[red]Please provide a symbol to remove.[/red]")
        return
    removed = wl.remove_symbol(symbol)
    if removed:
        console.print(f"[green]'{symbol.upper()}' removed from watchlist.[/green]")
    else:
        console.print(f"[yellow]'{symbol.upper()}' was not found in your watchlist.[/yellow]")


def handle_clear() -> None:
    """Handle clearing the entire watchlist."""
    wl.clear_watchlist()
    console.print("[green]Watchlist cleared.[/green]")
