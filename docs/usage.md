# Usage

## Basic Command

```bash
ubuntupy --project-path /path/to/python/project
```

Default output is JSON.

## Text Output

```bash
ubuntupy --project-path /path/to/python/project --output text
```

## Include Environment File

```bash
ubuntupy --project-path /path/to/python/project --env-file /path/to/.env
```

## JSON Config Override

Set `UBUNTUPY_CONFIG` to a JSON file that overrides defaults:

```json
{
  "preferred_versions": {
    "numpy": "1.26.4"
  },
  "blocked_versions": {
    "requests": ["2.19.0"]
  }
}
```

Example:

```bash
export UBUNTUPY_CONFIG=/path/to/ubuntupy-config.json
ubuntupy --project-path /path/to/python/project
```
