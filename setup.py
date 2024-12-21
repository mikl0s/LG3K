"""Setup script for the Log Generator 3000 package."""

from setuptools import find_packages, setup

setup(
    name="lg3k",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "rich==13.7.0",
    ],
    python_requires=">=3.12",
    author="Miklos",
    author_email="miklos@example.com",
    description="A versatile log generation tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mikl0s/LG3K",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)
