"""Optimizer for selecting preferred dependency versions."""

from __future__ import annotations

import re


class DependencyOptimizer:
    """Rank and select candidates based on basic policy."""

    def __init__(self, config: dict[str, object]):
        self.config = config

    @staticmethod
    def _version_key(version: str) -> tuple[int, ...]:
        parts = re.findall(r"\d+", version)
        if not parts:
            return (0,)
        return tuple(int(part) for part in parts)

    def choose(self, package_name: str, candidates: list[str]) -> str:
        blocked_versions = (
            self.config.get("blocked_versions", {}).get(package_name, set())  # type: ignore[union-attr]
        )
        safe_candidates = [candidate for candidate in candidates if candidate not in blocked_versions]
        if not safe_candidates:
            safe_candidates = candidates
        ranked = sorted(safe_candidates, key=self._version_key, reverse=True)
        return ranked[0] if ranked else "latest"
