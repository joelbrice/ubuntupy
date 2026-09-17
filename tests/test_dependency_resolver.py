import unittest

from ubuntupy.modules.ai_model.model import PredictionResponse
from ubuntupy.modules.dependency_resolver import DependencySolver


class DependencyResolverTests(unittest.TestCase):
    def test_solver_keeps_existing_pinned_versions(self):
        solver = DependencySolver()
        prediction = PredictionResponse(
            dependencies={"requests": "latest", "pandas": "latest"},
            model_name="local-fine-tunable",
        )

        result = solver.solve(existing_requirements={"requests": "2.31.0"}, prediction=prediction)

        self.assertEqual(result.dependencies["requests"], "2.31.0")
        self.assertEqual(result.dependencies["pandas"], "latest")
        self.assertTrue(any(note.startswith("Total dependencies") for note in result.notes))


if __name__ == "__main__":
    unittest.main()
