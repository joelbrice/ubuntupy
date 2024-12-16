from setuptools import setup, find_packages

setup(
    name='ubuntupy',
    version='0.1.0',
    description='AI-Powered Python Dependency Management',
    author='Joel Tiogo',
    author_email='tiogojoel@gmail.com',
    packages=find_packages(),
    install_requires=[
        # Add required packages here
    ],
    entry_points={
        'console_scripts': [
            'ubuntupy=ubuntupy.core:main',
        ],
    },
)
