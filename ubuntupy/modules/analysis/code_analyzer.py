"""Static code analyzer for Python projects."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def _parse_requirements(requirements_path: Path) -> dict[str, str]:
    dependencies: dict[str, str] = {}
    if not requirements_path.exists():
        return dependencies

    for raw_line in requirements_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line:
            name, version = line.split("==", 1)
            dependencies[name.strip()] = f"=={version.strip()}"
        else:
            dependencies[line] = "*"
    return dependencies


class CodeAnalyzer:
    """Analyze project source code and declared dependencies."""

    @staticmethod
    def _discover_local_modules(root: Path) -> set[str]:
        local_names: set[str] = set()
        for py_file in root.rglob("*.py"):
            if ".venv" in py_file.parts or "venv" in py_file.parts:
                continue
            local_names.add(py_file.stem)

        for child in root.iterdir():
            if child.is_dir() and (child / "__init__.py").exists():
                local_names.add(child.name)
        return local_names

    def analyze(self, project_path: str) -> dict[str, object]:
        root = Path(project_path)
        local_modules = self._discover_local_modules(root)
        stdlib_modules = set(getattr(sys, "stdlib_module_names", set()))
        imports: set[str] = set()

        for py_file in root.rglob("*.py"):
            if ".venv" in py_file.parts or "venv" in py_file.parts:
                continue
            try:
                module = ast.parse(py_file.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue

            for node in ast.walk(module):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split(".")[0]
                        if module_name not in stdlib_modules and module_name not in local_modules:
                            imports.add(module_name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    module_name = node.module.split(".")[0]
                    if module_name not in stdlib_modules and module_name not in local_modules:
                        imports.add(module_name)

        requirements = _parse_requirements(root / "requirements.txt")
        return {
            "imports": sorted(imports),
            "declared_dependencies": requirements,
        }
