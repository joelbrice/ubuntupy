"""Utilities for AI model package."""

from __future__ import annotations


def clamp_confidence(value: float) -> float:
    """Clamp confidence score to [0.0, 1.0]."""
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value
