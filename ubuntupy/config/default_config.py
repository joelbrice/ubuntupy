from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class LLMModelConfig:
    """Configuration for a single model backend."""

    name: str
    provider: str
    model: str
    temperature: float = 0.1
    max_tokens: int = 400
    api_key_env: str | None = None
    base_url: str | None = None
    enabled: bool = True


@dataclass(frozen=True)
class UbuntuPyConfig:
    """Application-level configuration."""

    default_model: str = "local-fine-tunable"
    models: Dict[str, LLMModelConfig] = field(default_factory=dict)
    allow_network_models: bool = False
    max_dependencies: int = 30


def load_default_config() -> UbuntuPyConfig:
    """Return production-safe defaults."""

    models = {
        "openai": LLMModelConfig(
            name="openai",
            provider="openai",
            model="gpt-4o-mini",
            api_key_env="OPENAI_API_KEY",
            enabled=True,
        ),
        "anthropic": LLMModelConfig(
            name="anthropic",
            provider="anthropic",
            model="claude-3-5-haiku-latest",
            api_key_env="ANTHROPIC_API_KEY",
            enabled=True,
        ),
        "local-fine-tunable": LLMModelConfig(
            name="local-fine-tunable",
            provider="local",
            model="distilbert-base-uncased",
            enabled=True,
        ),
    }
    return UbuntuPyConfig(models=models)
