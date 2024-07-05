# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.setrecursionlimit(1500)

current_dir = os.path.dirname(__file__)

projectPath = os.path.abspath(os.path.join(current_dir, "../src"))
sys.path.append(projectPath)

from generate_caption import ImageCaptionGenerator
from image_pipeline import Blip2Pipeline
year = datetime.datetime.now().year

project = "PulseMan"
copyright = f"{year}, Dipanjan Das, Sayantan Roy"
author = "Sayantan Roy, Dipanjan Das"


autoapi_dirs = ["../src"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",    
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.ifconfig",
    "sphinx_copybutton",
    #"sphinx.ext.autosummary",
]

autodoc_typehints = "description"
autodoc_class_signature = "separated"
autoapi_options = [
    "members",
    "undoc-members",
    "inherited-members",
    "private-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

# html_logo = '../resources/logo.png'

#pygments_style = "stata-dark"

#html_logo = "https://pydata.org/wp-content/uploads/2019/06/pydata-logo-final.png"
html_title = "PulseMan Docs"

#Using https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html

html_theme_options = {
    "use_edit_page_button": True,
    "back_to_top_button": True,
    #"repository_url": "https://github.com/Tech-Intelli/I2C_Source",
    #"use_repository_button": True, #for book theme
    #"max_navbar_depth": 2,         #for book theme
    #"collapse_navbar": True,       #for book theme
    "pygments_light_style": "tango",
    "pygments_dark_style": "monokai",
    "primary_sidebar_end": ["indices.html"],
    "secondary_sidebar_items": ["page-toc", "sourcelink"],  
    "show_toc_level": 1,
    "show_nav_level": 1,
    "navigation_depth": 2,
    "external_links": [
      {"name": "Source Code", "url": "https://github.com/Tech-Intelli/I2C_Source"}      
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Tech-Intelli/I2C_Source",  # required
            "icon": "fa-brands fa-square-github",
        },
        {
            "name": "Twitter",
            "url": "https://twitter.com/<your-handle>",
            "icon": "fa-brands fa-square-twitter",
        }
    ],
}

html_context = {
    # "github_url": "https://github.com", # or your GitHub Enterprise site
    "github_user": "google",
    "github_repo": "https://github.com/Tech-Intelli/I2C_Source",
    "github_version": "main",
    "doc_path": "<path-from-root-to-your-docs>",
}

add_module_names = False
# autodock_mock_imports = ['boto3']
# autodock_mock_imports = ['flask', 'ritetag ']
# The master toctree document.
# master_doc = "index"

suppress_warnings = ["autoapi.python_import_resolution", "autoapi.not_readable"]

# Napoleon settings
napoleon_google_docstring = True


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
# html_theme = "piccolo_theme"

html_static_path = ["_static"]
html_css_files = ["custom.css"]
