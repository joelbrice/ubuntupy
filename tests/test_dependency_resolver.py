import unittest

from ubuntupy.modules.dependency_resolver.solver import DependencySolver


class TestDependencySolver(unittest.TestCase):
    def test_solver_picks_highest_non_blocked_candidate(self):
        solver = DependencySolver(config={"blocked_versions": {"requests": {"2.32.3"}}})
        resolution = solver.resolve(
            {
                "requests": {
                    "candidates": ["2.31.0", "2.32.3"],
                    "confidence": 0.8,
                    "reason": "test",
                }
            }
        )
        self.assertEqual(resolution["resolved_dependencies"]["requests"], "2.31.0")
        self.assertIn("requests", resolution["conflicts"])

    def test_solver_handles_missing_candidates(self):
        solver = DependencySolver(config={})
        resolution = solver.resolve({"pkg": {"confidence": 0.1, "reason": "x"}})
        self.assertEqual(resolution["resolved_dependencies"]["pkg"], "latest")


if __name__ == "__main__":
    unittest.main()
