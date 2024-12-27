"""Setup script for LG3K."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lg3k",
    description="Log Generator 3000 - A modular log generation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.7.0",
    author="Mikkel Georgsen",
    author_email="lg3k@dataloes.dk",
    url="https://github.com/mikl0s/LG3K",
    packages=find_packages(exclude=["tests*", "docs*"]),
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
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Logging",
        "Topic :: System :: Systems Administration",
    ],
    keywords="log generator testing development monitoring",
)
