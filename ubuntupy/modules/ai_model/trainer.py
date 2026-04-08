"""Training placeholder for future ML model development."""

from __future__ import annotations


class ModelTrainer:
    """Placeholder interface for model-training workflows."""

    def fit(self, training_data: object) -> dict[str, object]:
        return {
            "status": "not_implemented",
            "message": "UbuntuPy currently uses a heuristic predictor.",
            "samples_seen": 0 if training_data is None else len(training_data),  # type: ignore[arg-type]
        }
