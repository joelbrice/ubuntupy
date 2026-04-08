"""Dependency resolution orchestrator."""

from __future__ import annotations

from .conflict_handler import ConflictHandler
from .optimizer import DependencyOptimizer


class DependencySolver:
    """Resolve dependency candidates into a single actionable plan."""

    def __init__(self, config: dict[str, object]):
        self.conflict_handler = ConflictHandler()
        self.optimizer = DependencyOptimizer(config)

    def resolve(self, predictions: dict[str, dict[str, object]]) -> dict[str, object]:
        resolved: dict[str, str] = {}
        conflicts: dict[str, list[str]] = {}

        for package_name, payload in predictions.items():
            raw_candidates = payload.get("candidates", ["latest"])
            candidates = raw_candidates if isinstance(raw_candidates, list) else ["latest"]
            candidates = [str(candidate) for candidate in candidates if str(candidate).strip()]
            if not candidates:
                candidates = ["latest"]

            package_conflicts = self.conflict_handler.find_conflicts(candidates)
            if package_conflicts:
                conflicts[package_name] = package_conflicts

            resolved[package_name] = self.optimizer.choose(package_name, candidates)

        return {
            "resolved_dependencies": resolved,
            "conflicts": conflicts,
            "count": len(resolved),
        }
