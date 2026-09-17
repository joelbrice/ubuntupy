from __future__ import annotations

import json
import os
from dataclasses import replace
from pathlib import Path
from typing import Any

from .default_config import LLMModelConfig, UbuntuPyConfig


class ConfigError(ValueError):
    """Raised when user configuration is invalid."""


def _read_json_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Config file does not exist: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON in config file: {path}") from exc

    if not isinstance(data, dict):
        raise ConfigError("Top-level config must be an object")

    return data


def _parse_models(raw_models: dict[str, Any], base_models: dict[str, LLMModelConfig]) -> dict[str, LLMModelConfig]:
    models = dict(base_models)
    for name, payload in raw_models.items():
        if not isinstance(payload, dict):
            raise ConfigError(f"Model entry '{name}' must be an object")

        base = models.get(name, LLMModelConfig(name=name, provider="local", model="distilbert-base-uncased"))
        models[name] = replace(
            base,
            provider=str(payload.get("provider", base.provider)),
            model=str(payload.get("model", base.model)),
            temperature=float(payload.get("temperature", base.temperature)),
            max_tokens=int(payload.get("max_tokens", base.max_tokens)),
            api_key_env=payload.get("api_key_env", base.api_key_env),
            base_url=payload.get("base_url", base.base_url),
            enabled=bool(payload.get("enabled", base.enabled)),
        )
    return models


def apply_user_config(base: UbuntuPyConfig, config_path: str | None) -> UbuntuPyConfig:
    """Apply optional user config and environment overrides."""

    data: dict[str, Any] = {}
    if config_path:
        data = _read_json_config(Path(config_path))

    models_data = data.get("models", {})
    if not isinstance(models_data, dict):
        raise ConfigError("'models' must be an object")

    models = _parse_models(models_data, base.models)

    merged = replace(
        base,
        default_model=str(data.get("default_model", base.default_model)),
        allow_network_models=bool(data.get("allow_network_models", base.allow_network_models)),
        max_dependencies=int(data.get("max_dependencies", base.max_dependencies)),
        models=models,
    )

    env_model = os.getenv("UBUNTUPY_DEFAULT_MODEL")
    env_network = os.getenv("UBUNTUPY_ALLOW_NETWORK_MODELS")
    if env_model:
        merged = replace(merged, default_model=env_model)
    if env_network is not None:
        merged = replace(merged, allow_network_models=env_network.lower() in {"1", "true", "yes"})

    if merged.default_model not in merged.models:
        raise ConfigError(f"Unknown default_model '{merged.default_model}'")

    return merged
