# UbuntuPy Architecture

## Architecture Review Summary

The repository originally contained mostly placeholders and partial scaffolding. The architecture has been refreshed into a complete MVP pipeline with clear module boundaries and executable behavior.

## High-Level Flow

1. **Code Analysis**
   - Parse Python imports.
   - Read declared dependencies from `requirements.txt`.
2. **Environment Analysis**
   - Capture runtime metadata.
   - Parse optional `.env` variables.
3. **Prediction Layer**
   - Build dependency candidates from declarations + imports.
   - Apply policy-driven preferred versions.
4. **Resolution Layer**
   - Detect candidate conflicts.
   - Select optimized versions with blocked-version safety checks.
5. **Presentation Layer**
   - Return structured recommendation report.
   - Emit JSON/text via CLI.

## Module Boundaries

- `ubuntupy/core.py`
  - orchestrates the full pipeline
  - provides CLI entrypoint and output formatting
- `ubuntupy/config`
  - default recommendation policy
  - deep-merge user overrides from JSON config
- `ubuntupy/modules/analysis`
  - `CodeAnalyzer`
  - `EnvAnalyzer`
- `ubuntupy/modules/ai_model`
  - `AIPredictor` (heuristic baseline)
  - model utility and training placeholders for future ML
- `ubuntupy/modules/dependency_resolver`
  - `ConflictHandler`
  - `DependencyOptimizer`
  - `DependencySolver`

## Design Principles

- **Explainability**: prediction payload includes confidence and reason.
- **Composability**: each stage can be tested independently.
- **Extensibility**: heuristic model can be replaced with learned models.
- **Safety-first defaults**: blocked versions avoid known-risk picks when alternatives exist.

## Extension Points

- Add `pyproject.toml` and lockfile analyzers.
- Integrate vulnerability feeds for real-time risk scoring.
- Replace heuristic ranking with ML/LLM-assisted ranking.
- Add plugin points for ecosystem-specific resolvers.
