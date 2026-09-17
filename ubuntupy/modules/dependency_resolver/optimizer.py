from __future__ import annotations


class DependencyOptimizer:
    """Apply deterministic ordering and output normalization."""

    @staticmethod
    def optimize(dependencies: dict[str, str]) -> dict[str, str]:
        return {name: dependencies[name] for name in sorted(dependencies)}
