import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from ubuntupy.core import build_recommendation, main


class TestCore(unittest.TestCase):
    def test_build_recommendation_returns_expected_shape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            (project / "app.py").write_text("import requests\nimport numpy\n", encoding="utf-8")
            (project / "requirements.txt").write_text("requests==2.31.0\n", encoding="utf-8")

            result = build_recommendation(str(project))

            self.assertIn("analysis", result)
            self.assertIn("predictions", result)
            self.assertIn("resolution", result)
            self.assertIn("requests", result["resolution"]["resolved_dependencies"])

    def test_main_outputs_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            (project / "code.py").write_text("import pandas\n", encoding="utf-8")

            stream = io.StringIO()
            with redirect_stdout(stream):
                exit_code = main(["-p", str(project), "--output", "json"])

            payload = json.loads(stream.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertIn("resolution", payload)


if __name__ == "__main__":
    unittest.main()
