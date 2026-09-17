from __future__ import annotations

from pathlib import Path


def write_requirements(project_path: str, dependencies: dict[str, str]) -> str:
    """Write dependencies to requirements.txt and return output path."""

    output_path = Path(project_path) / "requirements.txt"
    lines = [f"{name}=={version}" if version and version != "latest" else name for name, version in dependencies.items()]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(output_path)
