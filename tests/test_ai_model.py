import unittest

from ubuntupy.modules.ai_model.predictor import AIPredictor


class TestAIPredictor(unittest.TestCase):
    def test_predict_prefers_declared_exact_versions(self):
        predictor = AIPredictor(
            config={
                "preferred_versions": {"numpy": "1.26.4"},
            }
        )
        predictions = predictor.predict(
            code_analysis={
                "declared_dependencies": {"numpy": "==1.25.0"},
                "imports": ["numpy"],
            },
            env_analysis={},
        )

        self.assertEqual(predictions["numpy"]["candidates"][0], "1.25.0")
        self.assertEqual(predictions["numpy"]["confidence"], 0.95)

    def test_predict_maps_known_import_aliases(self):
        predictor = AIPredictor(config={"preferred_versions": {"opencv-python": "4.10.0"}})
        predictions = predictor.predict(
            code_analysis={"declared_dependencies": {}, "imports": ["cv2"]},
            env_analysis={},
        )
        self.assertIn("opencv-python", predictions)


if __name__ == "__main__":
    unittest.main()
