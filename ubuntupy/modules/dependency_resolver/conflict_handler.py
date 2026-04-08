"""Conflict detection and sanitization."""

from __future__ import annotations


class ConflictHandler:
    """Detect simple dependency conflict shapes."""

    def find_conflicts(self, candidates: list[str]) -> list[str]:
        unique = []
        for candidate in candidates:
            if candidate not in unique:
                unique.append(candidate)
        if len(unique) <= 1:
            return []
        return [f"Multiple candidate versions detected: {', '.join(unique)}"]
