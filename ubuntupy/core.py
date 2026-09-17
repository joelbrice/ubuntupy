from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict

from ubuntupy.config import load_config
from ubuntupy.modules.ai_model.predictor import AIPredictor
from ubuntupy.modules.analysis import CodeAnalyzer, EnvAnalyzer
from ubuntupy.modules.dependency_resolver import DependencySolver
from ubuntupy.modules.utils import configure_logging, write_requirements

LOGGER = logging.getLogger("ubuntupy")


def run(project_path: str, env_file: str | None = None, config_path: str | None = None, write: bool = False) -> dict:
    """Execute the dependency inference pipeline."""

    config = load_config(config_path=config_path)
    analyzer = CodeAnalyzer()
    env_analyzer = EnvAnalyzer()
    predictor = AIPredictor(config)
    solver = DependencySolver()

    code_result = analyzer.analyze(project_path)
    env_result = env_analyzer.analyze(project_path, env_file)

    prediction = predictor.predict_dependencies(
        imported_modules=code_result.imported_modules,
        existing_requirements=env_result.existing_requirements,
    )

    resolved = solver.solve(env_result.existing_requirements, prediction)
    result = {
        "project_path": project_path,
        "model": prediction.model_name,
        "dependencies": resolved.dependencies,
        "notes": resolved.notes,
        "environment": asdict(env_result),
    }

    if write:
        result["requirements_path"] = write_requirements(project_path, resolved.dependencies)

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="UbuntuPy: AI-Powered Python Dependency Management")
    parser.add_argument("-p", "--project-path", required=True, help="Path to the project directory")
    parser.add_argument("-e", "--env-file", help="Path to an optional .env file")
    parser.add_argument("-c", "--config", help="Path to ubuntupy JSON config")
    parser.add_argument("--write", action="store_true", help="Write resulting requirements.txt")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    configure_logging(args.log_level)

    try:
        output = run(
            project_path=args.project_path,
            env_file=args.env_file,
            config_path=args.config,
            write=args.write,
        )
    except Exception as exc:  # pragma: no cover - defensive top-level guard
        LOGGER.exception("Execution failed")
        raise SystemExit(1) from exc

    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
