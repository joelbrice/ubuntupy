import unittest

from ubuntupy.config.default_config import UbuntuPyConfig, load_default_config
from ubuntupy.modules.ai_model.predictor import AIPredictor
from ubuntupy.modules.ai_model.trainer import UbuntuPyFineTunableModel


class AIModelTests(unittest.TestCase):
    def test_predictor_exposes_available_models(self):
        config = load_default_config()
        predictor = AIPredictor(config)

        self.assertIn("openai", predictor.available_models)
        self.assertIn("anthropic", predictor.available_models)
        self.assertIn("local-fine-tunable", predictor.available_models)

    def test_local_model_can_train_and_predict(self):
        model = UbuntuPyFineTunableModel()
        model.bootstrap_from_open_source("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        model.fine_tune([{"requests", "pandas"}, {"requests"}])

        prediction = model.predict(
            type(
                "Req",
                (),
                {
                    "imported_modules": {"requests", "numpy"},
                    "existing_requirements": {"requests": "2.31.0"},
                    "max_dependencies": 10,
                },
            )()
        )

        self.assertEqual(prediction["requests"], "2.31.0")
        self.assertIn("numpy", prediction)

    def test_predictor_honors_default_model_choice(self):
        base = load_default_config()
        config = UbuntuPyConfig(
            default_model="openai",
            models=base.models,
            allow_network_models=False,
            max_dependencies=base.max_dependencies,
        )
        predictor = AIPredictor(config)

        response = predictor.predict_dependencies({"requests"}, {})
        self.assertEqual(response.model_name, "openai")
        self.assertIn("requests", response.dependencies)


if __name__ == "__main__":
    unittest.main()
