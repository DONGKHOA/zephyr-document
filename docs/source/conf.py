# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Tutorial Zephyr in UBUNTU'
copyright = '2024, DONGKHOA'
author = 'DONGKHOA'
release = 'ver 1.0.1'

# -- General configuration ---------------------------------------------------

extensions = ["sphinx_rtd_theme",]

templates_path = ['_templates']
exclude_patterns = []

language = 'vi'
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']