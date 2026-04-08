"""Configuration public API."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .default_config import DEFAULT_CONFIG
from .user_config import load_user_config


def _deep_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load merged configuration."""
    return _deep_merge(DEFAULT_CONFIG, load_user_config(config_path))


__all__ = ["load_config", "DEFAULT_CONFIG"]
