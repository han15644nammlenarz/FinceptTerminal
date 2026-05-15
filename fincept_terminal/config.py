"""Configuration management for FinceptTerminal."""

import os
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "theme": "dark",
    "refresh_interval": 60,
    "default_currency": "USD",
    "data_sources": {
        "stocks": "yahoo_finance",
        "crypto": "coingecko",
        "forex": "exchangerate"
    },
    "watchlist": [],
    "api_keys": {},
    "log_level": "INFO"
}

CONFIG_DIR = Path.home() / ".fincept"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir() -> None:
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load configuration from disk, falling back to defaults."""
    ensure_config_dir()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        merged = DEFAULT_CONFIG.copy()
        merged.update(user_config)
        return merged
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[WARNING] Failed to load config: {exc}. Using defaults.")
        return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    """Persist configuration to disk."""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except OSError as exc:
        print(f"[ERROR] Failed to save config: {exc}")


def get(key: str, default=None):
    """Retrieve a single configuration value by key."""
    return load_config().get(key, default)


def set_value(key: str, value) -> None:
    """Update a single configuration value and persist."""
    config = load_config()
    config[key] = value
    save_config(config)
