"""Heuristic AI predictor for dependency recommendations."""

from __future__ import annotations


IMPORT_TO_PACKAGE = {
    "sklearn": "scikit-learn",
    "cv2": "opencv-python",
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
}


class AIPredictor:
    """Predict dependency versions based on code, declarations, and policy."""

    def __init__(self, config: dict[str, object]):
        self.config = config

    def _canonical_package(self, import_name: str) -> str:
        return IMPORT_TO_PACKAGE.get(import_name, import_name)

    def predict(
        self,
        code_analysis: dict[str, object],
        env_analysis: dict[str, object],
    ) -> dict[str, dict[str, object]]:
        del env_analysis  # reserved for future model input

        declared = code_analysis.get("declared_dependencies", {})
        imports = code_analysis.get("imports", [])
        preferred = self.config.get("preferred_versions", {})
        predictions: dict[str, dict[str, object]] = {}

        for name, specifier in declared.items():
            version = (
                specifier.replace("==", "")
                if isinstance(specifier, str) and specifier.startswith("==")
                else preferred.get(name, "latest")
            )
            predictions[name] = {
                "candidates": [version],
                "confidence": 0.95 if specifier != "*" else 0.75,
                "reason": "declared dependency" if specifier != "*" else "preferred version",
            }

        for module_name in imports:
            package_name = self._canonical_package(module_name)
            if package_name in predictions:
                continue
            predictions[package_name] = {
                "candidates": [preferred.get(package_name, "latest")],
                "confidence": 0.60,
                "reason": "inferred from imports",
            }

        return predictions
