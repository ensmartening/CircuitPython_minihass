import datetime
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "CircuitPython minihass package"
creation_year = "2023"
current_year = str(datetime.datetime.now().year)
year_duration = (
    current_year
    if current_year == creation_year
    else creation_year + " - " + current_year
)
copyright = year_duration + " Adam Schumacher"
author = "Adam Schumacher"
release = "0.1.0-beta"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


# The master toctree document.
master_doc = "index"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    "CODE_OF_CONDUCT.md",
]
autoclass_content = "both"
# utodoc_inherit_docstrings = False
autoclass_signature = "separated"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "mmqtt": ("https://docs.circuitpython.org/projects/minimqtt/en/latest/", None),
    "CircuitPython": ("https://docs.circuitpython.org/en/latest/", None),
}
napoleon_google_docstrings = True
# intersphinx_disabled_reftypes = ["*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "piccolo_theme"
html_static_path = ["_static"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
#
default_role = "any"

# If true, '()' will be appended to :func: etc. cross-reference text.
#
add_function_parentheses = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# If this is True, todo emits a warning for each TODO entries. The default is False.
todo_emit_warnings = False

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#
html_favicon = "_static/favicon.ico"

# Output file base name for HTML help builder.
htmlhelp_basename = "CircuitPython_Minihass_Librarydoc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "CircuitPython_minihass_Library.tex",
        "CircuitPython minihass Library Documentation",
        author,
        "manual",
    ),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "CircuitPython_minihass_Library",
        "CircuitPython minihass Library Documentation",
        [author],
        1,
    ),
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "CircuitPython_minihass_Library",
        "CircuitPython minihass Library Documentation",
        author,
        "CircuitPython_minihass_Library",
        "One line description of project.",
        "Miscellaneous",
    ),
]
