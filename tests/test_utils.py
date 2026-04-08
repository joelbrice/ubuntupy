import json
import tempfile
import unittest
from pathlib import Path

from ubuntupy.config import DEFAULT_CONFIG, load_config
from ubuntupy.modules.analysis.code_analyzer import CodeAnalyzer
from ubuntupy.modules.analysis.env_analyzer import EnvAnalyzer


class TestConfig(unittest.TestCase):
    def test_load_config_merges_user_overrides(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text(
                json.dumps({"preferred_versions": {"numpy": "1.0.0"}}),
                encoding="utf-8",
            )
            merged = load_config(str(config_path))
            self.assertEqual(merged["preferred_versions"]["numpy"], "1.0.0")
            self.assertIn("objective_weights", merged)

    def test_default_config_available(self):
        self.assertIn("preferred_versions", DEFAULT_CONFIG)


class TestAnalyzers(unittest.TestCase):
    def test_code_analyzer_reads_imports_and_requirements(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            (project / "main.py").write_text("import requests\nfrom numpy import array\n", encoding="utf-8")
            (project / "requirements.txt").write_text("requests==2.31.0\n", encoding="utf-8")

            result = CodeAnalyzer().analyze(str(project))
            self.assertIn("requests", result["imports"])
            self.assertIn("numpy", result["imports"])
            self.assertEqual(result["declared_dependencies"]["requests"], "==2.31.0")

    def test_code_analyzer_ignores_stdlib_and_local_modules(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            (project / "local_mod.py").write_text("VALUE = 1\n", encoding="utf-8")
            (project / "main.py").write_text(
                "import os\nimport local_mod\nimport requests\n",
                encoding="utf-8",
            )
            result = CodeAnalyzer().analyze(str(project))
            self.assertIn("requests", result["imports"])
            self.assertNotIn("os", result["imports"])
            self.assertNotIn("local_mod", result["imports"])

    def test_env_analyzer_reads_dotenv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            dotenv = Path(temp_dir) / ".env"
            dotenv.write_text("FOO=bar\n# comment\n", encoding="utf-8")
            result = EnvAnalyzer().analyze(str(dotenv))
            self.assertEqual(result["env_vars"]["FOO"], "bar")


if __name__ == "__main__":
    unittest.main()
