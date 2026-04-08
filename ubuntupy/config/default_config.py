"""Default configuration for UbuntuPy."""

DEFAULT_CONFIG = {
    "objective_weights": {
        "security": 0.45,
        "performance": 0.35,
        "compatibility": 0.20,
    },
    "preferred_versions": {
        "numpy": "1.26.4",
        "pandas": "2.2.2",
        "scipy": "1.13.1",
        "requests": "2.32.3",
        "flask": "3.0.3",
        "fastapi": "0.115.0",
    },
    "blocked_versions": {
        "requests": {"2.19.0"},
    },
}
