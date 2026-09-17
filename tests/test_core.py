import json
import tempfile
import unittest
from pathlib import Path

from ubuntupy.core import run


class CorePipelineTests(unittest.TestCase):
    def test_run_pipeline_returns_expected_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "app.py").write_text("import requests\nimport pandas\n", encoding="utf-8")
            (tmp_path / "requirements.txt").write_text("requests==2.31.0\n", encoding="utf-8")

            result = run(project_path=str(tmp_path))

            self.assertTrue(result["model"])
            self.assertIn("dependencies", result)
            self.assertEqual(result["dependencies"]["requests"], "2.31.0")
            self.assertIn("pandas", result["dependencies"])

    def test_run_writes_requirements(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "app.py").write_text("import flask\n", encoding="utf-8")

            result = run(project_path=str(tmp_path), write=True)

            output_path = Path(result["requirements_path"])
            self.assertTrue(output_path.exists())
            self.assertIn("flask", output_path.read_text(encoding="utf-8"))
            json.dumps(result)


if __name__ == "__main__":
    unittest.main()
