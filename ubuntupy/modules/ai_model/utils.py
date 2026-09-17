from __future__ import annotations

STANDARD_LIBRARY_MODULES = {
    "abc", "argparse", "asyncio", "collections", "csv", "datetime", "functools", "itertools",
    "json", "logging", "math", "os", "pathlib", "re", "subprocess", "sys", "typing", "unittest",
}


IMPORT_TO_PACKAGE_MAP = {
    "yaml": "pyyaml",
    "PIL": "pillow",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "bs4": "beautifulsoup4",
}


def normalize_package_name(module_name: str) -> str | None:
    """Map imported module names to PyPI package names."""

    if module_name in STANDARD_LIBRARY_MODULES:
        return None
    return IMPORT_TO_PACKAGE_MAP.get(module_name, module_name.lower().replace("_", "-"))
