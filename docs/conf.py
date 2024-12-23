"""Sphinx configuration for LG3K documentation."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "LG3K"
copyright = "2024, mikl0s"
author = "mikl0s"

# The full version, including alpha/beta/rc tags
release = "0.6.5"
# The short X.Y version
version = "0.6.5"

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
