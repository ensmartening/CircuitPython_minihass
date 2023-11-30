import sys
import os
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

extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx"]

templates_path = ["_templates"]
exclude_patterns = []
autoclass_content = "both"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "mmqtt": ("https://docs.circuitpython.org/projects/minimqtt/en/latest/", None),
}
# intersphinx_disabled_reftypes = ["*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
