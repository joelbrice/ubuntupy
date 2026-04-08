# Contributing Guide

## Ways to Contribute

- improve analyzers (imports/dependency extraction)
- improve predictor quality and explainability
- improve conflict handling and optimizer policies
- expand test coverage
- improve documentation clarity

## Development Workflow

1. Create a branch.
2. Implement focused changes.
3. Add or update tests.
4. Run test suite:

```bash
python -m unittest discover -s tests -v
```

5. Update documentation for behavior changes.
6. Open a pull request describing:
   - motivation
   - implementation
   - validation

## Quality Bar

- clear module boundaries
- deterministic behavior
- tests for each changed behavior
- no regressions in existing functionality
