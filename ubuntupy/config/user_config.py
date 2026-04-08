"""User configuration loader for UbuntuPy."""

from __future__ import annotations

import json
import os
from typing import Any


def load_user_config(config_path: str | None = None) -> dict[str, Any]:
    """
    Load user configuration from JSON.

    When config_path is not provided, UBUNTUPY_CONFIG is used if set.
    """
    chosen_path = config_path or os.getenv("UBUNTUPY_CONFIG")
    if not chosen_path:
        return {}

    if not os.path.exists(chosen_path):
        return {}

    with open(chosen_path, "r", encoding="utf-8") as config_file:
        return json.load(config_file)
