from __future__ import annotations

from dataclasses import dataclass

from ubuntupy.modules.ai_model.model import PredictionResponse

from .conflict_handler import ConflictHandler
from .optimizer import DependencyOptimizer


@dataclass
class SolverOutput:
    dependencies: dict[str, str]
    notes: list[str]


class DependencySolver:
    """Merge existing requirements and predicted dependencies."""

    def __init__(self) -> None:
        self._conflict_handler = ConflictHandler()
        self._optimizer = DependencyOptimizer()

    def solve(self, existing_requirements: dict[str, str], prediction: PredictionResponse) -> SolverOutput:
        merged = dict(existing_requirements)
        for package, predicted_version in prediction.dependencies.items():
            current = merged.get(package, "")
            merged[package] = self._conflict_handler.resolve(current, predicted_version)

        optimized = self._optimizer.optimize(merged)
        notes = list(prediction.notes)
        notes.append(f"Total dependencies: {len(optimized)}")
        return SolverOutput(dependencies=optimized, notes=notes)
