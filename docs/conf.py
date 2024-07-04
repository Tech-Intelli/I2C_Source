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

year = datetime.datetime.now().year
project = "PulseMan"

copyright = f"{year}, Dipanjan Das, Sayantan Roy, "

author = "Sayantan Roy, Dipanjan Das"
autoapi_dirs = ["../src"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.ifconfig",
]
# html_logo = '../resources/logo.png'

pygments_style = "stata-dark"

html_theme_options = {
    "banner_text": ("Made with love and passion by Dipanjan and Sayantan. "),
    "banner_hiding": "permanent",
    "show_theme_credit": False,
    "dark_mode_code_blocks": True,
    "source_url": "https://github.com/Tech-Intelli/I2C_Source",
    "source_icon": "github",
}

add_module_names = False
# autodock_mock_imports = ['boto3']
# autodock_mock_imports = ['flask', 'ritetag ']
# The master toctree document.
master_doc = "index"

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'sphinx_rtd_theme'
html_theme = "piccolo_theme"

html_static_path = ["_static"]
