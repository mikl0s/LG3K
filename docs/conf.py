"""Sphinx configuration for LG3K documentation."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "Log Generator 3000"
copyright = "2024, Mikkel Munch Mortensen"
author = "Mikkel Munch Mortensen"

# The full version, including alpha/beta/rc tags
release = "0.6.2"
# The short X.Y version
version = "0.6.2"

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
