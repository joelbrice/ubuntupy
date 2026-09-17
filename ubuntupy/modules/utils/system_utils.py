from __future__ import annotations

import platform


def runtime_summary() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
