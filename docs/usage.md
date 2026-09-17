# Usage

## Analyze and print recommendations

```bash
ubuntupy --project-path /path/to/project
```

## Analyze and write requirements file

```bash
ubuntupy --project-path /path/to/project --write
```

## Provide custom config

```bash
ubuntupy --project-path /path/to/project --config /path/to/ubuntupy.config.json
```

## Output

The CLI prints structured JSON including:

- selected model
- resolved dependencies
- environment summary
- processing notes
