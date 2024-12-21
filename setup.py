"""Setup script for LG3K."""

from setuptools import find_packages, setup

setup(
    name="lg3k",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.7",
        "pyyaml>=6.0.1",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "lg3k=lg3k.main:main",
        ],
    },
    author="mikl0s",
    author_email="mikl0s@example.com",
    description="A versatile log generation tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mikl0s/lg3k",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
