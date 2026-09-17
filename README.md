# UbuntuPy

UbuntuPy is a production-ready Python dependency intelligence tool with a clean, extensible architecture.
It analyzes project imports and environment signals, predicts dependencies through pluggable LLM providers, resolves conflicts, and can write a normalized `requirements.txt`.

## Highlights

- **Layered architecture** (analysis → model inference → dependency resolution)
- **Multi-model support** (OpenAI-compatible, Anthropic-compatible, local model)
- **Built-in local fine-tunable model** bootstrapped from open-source checkpoints
- **Deterministic conflict handling** and dependency ordering
- **Typed, testable modules** with clear extension points

## Architecture at a glance

- `ubuntupy/core.py`: Application orchestration and CLI entrypoint
- `ubuntupy/config/`: Default config + user/env config merge
- `ubuntupy/modules/analysis/`: Static code and environment analysis
- `ubuntupy/modules/ai_model/`: Model interfaces, provider registry, local fine-tunable model
- `ubuntupy/modules/dependency_resolver/`: Conflict resolution and optimization
- `ubuntupy/modules/utils/`: Logging and requirements file IO

See `docs/architecture.md` for detailed architecture.

## Installation

```bash
pip install -e .
```

## CLI usage

```bash
ubuntupy --project-path /path/to/project
```

Write `requirements.txt` directly:

```bash
ubuntupy --project-path /path/to/project --write
```

Use a custom config file:

```bash
ubuntupy --project-path /path/to/project --config /path/to/ubuntupy.config.json
```

## Configuration

UbuntuPy ships with three configured models:

- `openai`
- `anthropic`
- `local-fine-tunable` (default)

Override defaults with `ubuntupy.config.json`:

```json
{
  "default_model": "local-fine-tunable",
  "allow_network_models": false,
  "max_dependencies": 30,
  "models": {
    "local-fine-tunable": {
      "provider": "local",
      "model": "distilbert-base-uncased",
      "enabled": true
    }
  }
}
```

Environment overrides:

- `UBUNTUPY_CONFIG`
- `UBUNTUPY_DEFAULT_MODEL`
- `UBUNTUPY_ALLOW_NETWORK_MODELS`

## Local fine-tunable model

UbuntuPy includes `UbuntuPyFineTunableModel`, which:

1. Boots from an open-source base model identifier (metadata)
2. Learns package frequency from training corpora
3. Produces dependency predictions merged with existing pinned versions

This gives teams an auditable, offline-capable model path while keeping interfaces compatible with external LLM providers.

## Quality and standards

- Strong typing and dataclasses
- Clear module boundaries and single responsibility
- Deterministic outputs for reproducibility
- Unit tests for critical paths

Run tests:

```bash
pytest -q
```

## Documentation

- `docs/index.md`
- `docs/installation.md`
- `docs/usage.md`
- `docs/architecture.md`
- `docs/contributing.md`
