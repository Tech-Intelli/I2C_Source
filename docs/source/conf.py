"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
-- Project information -----------------------------------------------------
https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""

PROJECT = 'main'
COPYRIGHT = '2024, Dipanjan Das and Sayantan Roy'
AUTHOR = 'Sayantan Roy'
RELEASE = 'N/A'
HTML_THEME = 'alabaster'

extensions = [
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = []

html_static_path = ['_static']
