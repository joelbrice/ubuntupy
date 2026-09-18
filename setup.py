from setuptools import find_packages, setup

setup(
    name="ubuntupy",
    version="0.2.0",
    description="Production-ready AI-assisted Python dependency management",
    author="Joel Tiogo",
    author_email="tiogojoel@gmail.com",
    packages=find_packages(exclude=("tests", "docs")),
    python_requires=">=3.10",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ubuntupy=ubuntupy.core:main",
        ],
    },
)
