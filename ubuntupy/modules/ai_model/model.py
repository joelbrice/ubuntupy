"""Model abstractions for UbuntuPy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PredictionMetadata:
    package: str
    confidence: float
    reason: str
