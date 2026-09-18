from __future__ import annotations

import os

from .default_config import UbuntuPyConfig, load_default_config
from .user_config import apply_user_config


def load_config(config_path: str | None = None) -> UbuntuPyConfig:
    """Load merged default, user and environment configuration."""

    base = load_default_config()
    path = config_path or os.getenv("UBUNTUPY_CONFIG")
    return apply_user_config(base, path)


__all__ = ["UbuntuPyConfig", "load_config"]
