import tempfile
import unittest
from pathlib import Path

from ubuntupy.modules.analysis import CodeAnalyzer, EnvAnalyzer
from ubuntupy.modules.utils import write_requirements


class UtilsTests(unittest.TestCase):
    def test_code_analyzer_collects_imports(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            file_path = tmp_path / "main.py"
            file_path.write_text("import requests\nfrom pandas import DataFrame\n", encoding="utf-8")

            result = CodeAnalyzer().analyze(str(tmp_path))

            self.assertEqual(result.imported_modules, {"requests", "pandas"})

    def test_env_analyzer_reads_existing_requirements(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "requirements.txt").write_text("requests==2.31.0\npytest\n", encoding="utf-8")

            result = EnvAnalyzer().analyze(str(tmp_path))

            self.assertEqual(result.existing_requirements["requests"], "2.31.0")
            self.assertEqual(result.existing_requirements["pytest"], "")

    def test_write_requirements_formats_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = write_requirements(tmp, {"pytest": "", "requests": "2.31.0"})
            contents = Path(output).read_text(encoding="utf-8")

            self.assertIn("requests==2.31.0", contents)
            self.assertIn("pytest", contents)


if __name__ == "__main__":
    unittest.main()
