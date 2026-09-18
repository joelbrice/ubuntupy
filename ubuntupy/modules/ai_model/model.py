from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class PredictionRequest:
    imported_modules: set[str]
    existing_requirements: dict[str, str]
    max_dependencies: int = 30


@dataclass
class PredictionResponse:
    dependencies: dict[str, str]
    model_name: str
    notes: list[str] = field(default_factory=list)


class LLMModel(Protocol):
    name: str

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        ...
