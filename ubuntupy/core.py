import argparse
import json

from ubuntupy.modules.analysis import CodeAnalyzer, EnvAnalyzer
from ubuntupy.modules.ai_model.predictor import AIPredictor
from ubuntupy.modules.dependency_resolver.solver import DependencySolver
from ubuntupy.config import load_config


def build_recommendation(project_path: str, env_file: str | None = None) -> dict[str, object]:
    """Build a dependency recommendation report."""
    config = load_config()
    code_analyzer = CodeAnalyzer()
    env_analyzer = EnvAnalyzer()
    predictor = AIPredictor(config=config)
    solver = DependencySolver(config=config)

    code_analysis = code_analyzer.analyze(project_path)
    env_analysis = env_analyzer.analyze(env_file)
    predictions = predictor.predict(code_analysis=code_analysis, env_analysis=env_analysis)
    resolution = solver.resolve(predictions)
    return {
        "project_path": project_path,
        "analysis": {
            "imports_detected": code_analysis["imports"],
            "declared_dependencies": code_analysis["declared_dependencies"],
            "environment": env_analysis,
        },
        "predictions": predictions,
        "resolution": resolution,
    }


def main(argv: list[str] | None = None) -> int:
    """UbuntuPy CLI entrypoint."""
    parser = argparse.ArgumentParser(description="UbuntuPy: AI-Powered Python Dependency Management")
    parser.add_argument("-p", "--project-path", required=True, help="Path to the project directory")
    parser.add_argument("-e", "--env-file", help="Path to the .env file")
    parser.add_argument(
        "--output",
        choices=("json", "text"),
        default="json",
        help="Output format",
    )
    args = parser.parse_args(argv)

    recommendation = build_recommendation(project_path=args.project_path, env_file=args.env_file)
    if args.output == "json":
        print(json.dumps(recommendation, indent=2, sort_keys=True))
    else:
        resolved = recommendation["resolution"]["resolved_dependencies"]
        print("UbuntuPy recommended dependency plan:")
        for package_name, version in sorted(resolved.items()):
            print(f"- {package_name}=={version}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
