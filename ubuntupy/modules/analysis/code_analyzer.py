from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CodeAnalysisResult:
    project_path: str
    imported_modules: set[str] = field(default_factory=set)


class CodeAnalyzer:
    """Static Python import analyzer for dependency inference."""

    def analyze(self, project_path: str) -> CodeAnalysisResult:
        base = Path(project_path)
        result = CodeAnalysisResult(project_path=project_path)

        for file_path in base.rglob("*.py"):
            self._collect_imports(file_path, result)

        return result

    @staticmethod
    def _collect_imports(file_path: Path, result: CodeAnalysisResult) -> None:
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError, SyntaxError):
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result.imported_modules.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                result.imported_modules.add(node.module.split(".")[0])
