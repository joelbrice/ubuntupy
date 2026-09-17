from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .model import PredictionRequest
from .utils import normalize_package_name


@dataclass
class UbuntuPyFineTunableModel:
    """Local trainable model that can be bootstrapped from open-source checkpoints."""

    model_name: str = "local-fine-tunable"
    base_open_source_model: str = "distilbert-base-uncased"
    package_frequency: dict[str, int] = field(default_factory=dict)

    def bootstrap_from_open_source(self, model_name: str) -> None:
        """Set the open-source base model reference used for fine-tuning."""

        self.base_open_source_model = model_name

    def fine_tune(self, corpus: list[set[str]]) -> None:
        """Fine-tune by learning frequently used dependencies from import corpora."""

        for imports in corpus:
            for module in imports:
                package = normalize_package_name(module)
                if package:
                    self.package_frequency[package] = self.package_frequency.get(package, 0) + 1

    def predict(self, request: PredictionRequest) -> dict[str, str]:
        ranked = sorted(self.package_frequency.items(), key=lambda item: item[1], reverse=True)
        learned = [name for name, _ in ranked]

        inferred: list[str] = []
        for module in sorted(request.imported_modules):
            package = normalize_package_name(module)
            if package and package not in inferred:
                inferred.append(package)

        ordered = learned + [name for name in inferred if name not in learned]
        selected = ordered[: request.max_dependencies]
        return {name: request.existing_requirements.get(name, "latest") for name in selected}

    def save(self, path: str) -> None:
        payload = {
            "base_open_source_model": self.base_open_source_model,
            "package_frequency": self.package_frequency,
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str) -> "UbuntuPyFineTunableModel":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            base_open_source_model=str(payload.get("base_open_source_model", "distilbert-base-uncased")),
            package_frequency={str(k): int(v) for k, v in payload.get("package_frequency", {}).items()},
        )
