# UbuntuPy

UbuntuPy is an AI-assisted Python dependency recommendation tool focused on:

- intelligent dependency version prediction
- conflict-aware resolution
- security- and compatibility-conscious optimization
- practical CLI workflows for developers

## Why UbuntuPy

Python dependency management is often fragmented across source imports, requirements files, and runtime constraints. UbuntuPy unifies these signals and produces a single dependency recommendation plan.

## Current Capabilities

1. **Code analysis**
   - scans Python imports
   - reads declared dependencies from `requirements.txt`
2. **Environment analysis**
   - captures Python/runtime platform context
   - ingests optional `.env` variables
3. **AI-driven prediction (heuristic baseline)**
   - converts imports and declarations into package candidates
   - applies policy-based preferred versions
4. **Conflict resolution and optimization**
   - detects multi-candidate conflicts
   - selects safe candidates while honoring blocked versions
5. **CLI output**
   - emits machine-readable JSON or simple text plans

## Quick Start

```bash
python -m ubuntupy.core --project-path /path/to/project --output json
```

Or after install:

```bash
ubuntupy --project-path /path/to/project --output text
```

## Example Output (text mode)

```text
UbuntuPy recommended dependency plan:
- numpy==1.26.4
- requests==2.31.0
```

## Architecture Summary

UbuntuPy uses a modular pipeline:

`analysis -> prediction -> resolution -> recommendation`

- `ubuntupy/modules/analysis`: source and runtime context extraction
- `ubuntupy/modules/ai_model`: prediction logic and model abstractions
- `ubuntupy/modules/dependency_resolver`: conflict handling and optimization
- `ubuntupy/core.py`: CLI orchestration and report construction
- `ubuntupy/config`: default policy + optional user override merge

Full details: `docs/architecture.md`

## Documentation

- Project docs: `docs/index.md`
- Installation: `docs/installation.md`
- Usage: `docs/usage.md`
- Architecture: `docs/architecture.md`
- Contribution guide: `docs/contributing.md`

## Contributing

We welcome architecture improvements, resolver enhancements, and better predictive models. See:

- `CONTRIBUTING.md`
- `docs/contributing.md`
