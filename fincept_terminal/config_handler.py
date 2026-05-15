"""CLI handler for viewing and editing FinceptTerminal configuration."""

import json
from fincept_terminal.config import load_config, save_config, set_value, CONFIG_FILE


def show_config() -> None:
    """Print the current configuration to stdout."""
    config = load_config()
    print("\n=== FinceptTerminal Configuration ===")
    print(json.dumps(config, indent=2))
    print(f"\nConfig file: {CONFIG_FILE}")


def update_config(key: str, value: str) -> None:
    """
    Update a configuration key with the given string value.
    Attempts to parse the value as JSON for type coercion.
    """
    try:
        parsed_value = json.loads(value)
    except json.JSONDecodeError:
        parsed_value = value  # treat as plain string

    set_value(key, parsed_value)
    print(f"[OK] '{key}' updated to: {parsed_value}")


def reset_config() -> None:
    """Reset configuration to factory defaults."""
    from fincept_terminal.config import DEFAULT_CONFIG
    save_config(DEFAULT_CONFIG)
    print("[OK] Configuration reset to defaults.")


def add_to_watchlist(symbol: str) -> None:
    """Add a ticker symbol to the watchlist."""
    config = load_config()
    watchlist: list = config.get("watchlist", [])
    symbol = symbol.upper().strip()
    if symbol in watchlist:
        print(f"[INFO] '{symbol}' is already in the watchlist.")
        return
    watchlist.append(symbol)
    config["watchlist"] = watchlist
    save_config(config)
    print(f"[OK] Added '{symbol}' to watchlist.")


def remove_from_watchlist(symbol: str) -> None:
    """Remove a ticker symbol from the watchlist."""
    config = load_config()
    watchlist: list = config.get("watchlist", [])
    symbol = symbol.upper().strip()
    if symbol not in watchlist:
        print(f"[INFO] '{symbol}' not found in watchlist.")
        return
    watchlist.remove(symbol)
    config["watchlist"] = watchlist
    save_config(config)
    print(f"[OK] Removed '{symbol}' from watchlist.")


def set_api_key(provider: str, key: str) -> None:
    """Store an API key for a given provider."""
    config = load_config()
    api_keys: dict = config.get("api_keys", {})
    api_keys[provider.lower()] = key
    config["api_keys"] = api_keys
    save_config(config)
    print(f"[OK] API key for '{provider}' saved.")
