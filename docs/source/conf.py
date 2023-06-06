# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import shutil
import glob

sys.path.insert(0, os.path.abspath('../../compositionspace/'))

def skip(app, what, name, obj, would_skip, options):
    if name in ( '__init__',):
        return False
    return would_skip
def setup(app):
    app.connect('autodoc-skip-member', skip)

if os.path.exists("example"):
    shutil.rmtree("example")
shutil.copytree("../../example", "example")

project = 'compositionspace'
copyright = '2022, Alaukik Saxena, Sarath Menon'
author = 'Alaukik Saxena, Sarath Menon'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'm2r2',
    'sphinx_markdown_tables',
    'nbsphinx',
]

html_theme = 'furo'

html_theme_options = {
    #'logo_only' : True,
    #'canonical_url' : 'https://calphy.readthedocs.io/',
}

html_extra_path = ['../_static' ]

source_suffix = ['.rst', '.md']

exclude_patterns = []