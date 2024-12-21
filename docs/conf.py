"""Sphinx configuration for LG3K documentation."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "Log Generator 3000"
copyright = "2024, Miklos"
author = "Miklos"
version = "0.1.0"
release = "0.1.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output options
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# autodoc configuration
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "undoc-members": True,
}
