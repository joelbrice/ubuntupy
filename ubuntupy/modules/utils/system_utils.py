"""System utility helpers."""

from __future__ import annotations

import platform
import sys


def runtime_info() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": sys.platform,
    }
