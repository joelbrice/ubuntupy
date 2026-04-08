# Contributing to UbuntuPy

Thank you for your interest in improving UbuntuPy.

## Project Goals

- make Python dependency recommendations explainable
- improve conflict resolution quality
- optimize for security, performance, and compatibility
- keep workflows simple for users and contributors

## Development Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install local package:

```bash
pip install -e .
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Coding Guidelines

- Keep changes focused and modular.
- Prefer clear naming and small functions.
- Preserve backward-compatible CLI behavior where possible.
- Add/adjust tests for new behavior.

## Documentation Expectations

When behavior changes, update:

- `README.md`
- relevant files in `docs/`

## Suggested Contribution Areas

- richer dependency parsing (`pyproject.toml`, lock files)
- stronger conflict detection strategies
- learned ranking models for dependency scoring
- ecosystem-specific security policy integration

## Pull Requests

Please include:

- what problem is solved
- what changed
- how it was validated
