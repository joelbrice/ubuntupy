from __future__ import annotations

import os
import platform
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class EnvironmentAnalysisResult:
    python_version: str
    platform: str
    env_vars: dict[str, str] = field(default_factory=dict)
    existing_requirements: dict[str, str] = field(default_factory=dict)


class EnvAnalyzer:
    """Collect runtime and project environment metadata."""

    SAFE_ENV_KEYS = ("CI", "PYTHONPATH", "VIRTUAL_ENV")

    def analyze(self, project_path: str, env_file: str | None = None) -> EnvironmentAnalysisResult:
        env_vars = {key: os.getenv(key, "") for key in self.SAFE_ENV_KEYS if os.getenv(key)}
        existing = self._read_requirements(Path(project_path) / "requirements.txt")

        if env_file:
            env_vars.update(self._read_dotenv(Path(env_file)))

        return EnvironmentAnalysisResult(
            python_version=platform.python_version(),
            platform=platform.platform(),
            env_vars=env_vars,
            existing_requirements=existing,
        )

    @staticmethod
    def _read_dotenv(path: Path) -> dict[str, str]:
        if not path.exists():
            return {}

        values: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
        return values

    @staticmethod
    def _read_requirements(path: Path) -> dict[str, str]:
        if not path.exists():
            return {}

        reqs: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            raw = line.strip()
            if not raw or raw.startswith("#"):
                continue
            if "==" in raw:
                name, version = raw.split("==", 1)
                reqs[name.strip()] = version.strip()
            else:
                reqs[raw] = ""
        return reqs
