from __future__ import annotations

from dataclasses import dataclass

from ubuntupy.config.default_config import LLMModelConfig, UbuntuPyConfig

from .model import LLMModel, PredictionRequest, PredictionResponse
from .trainer import UbuntuPyFineTunableModel
from .utils import normalize_package_name


@dataclass
class HeuristicRemoteModel:
    """Non-network fallback model for configured remote providers."""

    name: str

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        deps: dict[str, str] = {}
        for module in sorted(request.imported_modules):
            package = normalize_package_name(module)
            if package:
                deps[package] = request.existing_requirements.get(package, "latest")
            if len(deps) >= request.max_dependencies:
                break
        return PredictionResponse(
            dependencies=deps,
            model_name=self.name,
            notes=["Heuristic inference used for remote provider compatibility."],
        )


class LocalFineTunableProvider:
    """Provider that wraps UbuntuPy's trainable local model."""

    def __init__(self, model: UbuntuPyFineTunableModel | None = None) -> None:
        self._model = model or UbuntuPyFineTunableModel()
        self.name = self._model.model_name

    def train_from_project_imports(self, project_imports: set[str]) -> None:
        self._model.fine_tune([project_imports])

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        deps = self._model.predict(request)
        return PredictionResponse(
            dependencies=deps,
            model_name=self.name,
            notes=[f"Bootstrapped from open-source model '{self._model.base_open_source_model}'."],
        )


class AIPredictor:
    """Model registry and prediction façade."""

    def __init__(self, config: UbuntuPyConfig) -> None:
        self._config = config
        self._models: dict[str, LLMModel] = self._build_registry(config)

    @staticmethod
    def _build_registry(config: UbuntuPyConfig) -> dict[str, LLMModel]:
        registry: dict[str, LLMModel] = {}
        for name, model_config in config.models.items():
            if not model_config.enabled:
                continue
            registry[name] = AIPredictor._build_provider(model_config)

        return registry

    @staticmethod
    def _build_provider(model_config: LLMModelConfig) -> LLMModel:
        if model_config.provider == "local":
            local = LocalFineTunableProvider()
            local._model.bootstrap_from_open_source(model_config.model)
            return local
        return HeuristicRemoteModel(name=model_config.name)

    def predict_dependencies(self, imported_modules: set[str], existing_requirements: dict[str, str]) -> PredictionResponse:
        if self._config.default_model not in self._models:
            raise ValueError(f"Model '{self._config.default_model}' is unavailable")

        request = PredictionRequest(
            imported_modules=imported_modules,
            existing_requirements=existing_requirements,
            max_dependencies=self._config.max_dependencies,
        )
        return self._models[self._config.default_model].predict(request)

    @property
    def available_models(self) -> list[str]:
        return sorted(self._models.keys())
