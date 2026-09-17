from __future__ import annotations


class ConflictHandler:
    """Resolve version conflicts using predictable precedence rules."""

    @staticmethod
    def resolve(existing_version: str, predicted_version: str) -> str:
        if existing_version and existing_version != "latest":
            return existing_version
        return predicted_version or "latest"
