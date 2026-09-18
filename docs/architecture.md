# Architecture

UbuntuPy follows a layered architecture designed for maintainability and production reliability.

## Layers

1. **Core orchestration (`ubuntupy/core.py`)**
   - Validates inputs
   - Initializes all services
   - Executes pipeline and renders output

2. **Configuration (`ubuntupy/config`)**
   - Provides secure defaults
   - Applies user JSON config
   - Supports environment overrides

3. **Analysis (`ubuntupy/modules/analysis`)**
   - `CodeAnalyzer`: parses Python imports with AST
   - `EnvAnalyzer`: collects runtime metadata and requirements baseline

4. **Model inference (`ubuntupy/modules/ai_model`)**
   - Shared prediction contract (`PredictionRequest/PredictionResponse`)
   - Provider registry for multiple model backends
   - Local fine-tunable model based on open-source model metadata

5. **Dependency resolution (`ubuntupy/modules/dependency_resolver`)**
   - Conflict handling that preserves pinned versions
   - Deterministic sorted output

6. **Utilities (`ubuntupy/modules/utils`)**
   - Logging configuration
   - Requirements file writing

## Data flow

`CodeAnalyzer + EnvAnalyzer -> AIPredictor -> DependencySolver -> optional requirements.txt write`

## Extensibility model

- Add a new provider by implementing the `LLMModel` protocol.
- Register it through configuration.
- Keep all provider-specific behavior inside `modules/ai_model`.
