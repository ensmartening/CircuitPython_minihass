import os
import sys

import minihass

sys.path.insert(0, os.path.abspath("../"))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "minihass"
copyright = "2023, Adam Schumacher"
author = "Adam Schumacher"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = []
autoclass_content = "both"
# utodoc_inherit_docstrings = False
autoclass_signature = "separated"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "mmqtt": ("https://docs.circuitpython.org/projects/minimqtt/en/latest/", None),
}
napoleon_google_docstrings = True
# intersphinx_disabled_reftypes = ["*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "piccolo_theme"
html_static_path = ["_static"]
