"""Environment analyzer."""

from __future__ import annotations

import os
import platform
import sys
from pathlib import Path


class EnvAnalyzer:
    """Extract runtime and optional .env context."""

    def analyze(self, env_file: str | None = None) -> dict[str, object]:
        dotenv_vars: dict[str, str] = {}
        if env_file:
            dotenv_path = Path(env_file)
            if dotenv_path.exists():
                for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
                    line = raw_line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    dotenv_vars[key.strip()] = value.strip()

        return {
            "python_version": platform.python_version(),
            "platform": sys.platform,
            "env_vars": dotenv_vars,
            "cpu_count": os.cpu_count() or 1,
        }
