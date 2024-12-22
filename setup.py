"""Setup script for LG3K."""

from setuptools import find_packages, setup

setup(
    name="lg3k",
    description="Log Generator 3000 - A modular log generation tool",
    version="0.6.2",
    author="Mikkel Munch Mortensen",
    author_email="lg3k@dataloes.dk",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "lg3k=lg3k.main:main",
        ],
    },
    python_requires=">=3.12",
)
