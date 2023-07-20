# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from git import Repo

sys.path.insert(0, os.path.abspath("../../"))
print(os.path.abspath("../../"))

project = 'Moildev'
copyright = '2023, Perseverance Technology'
author = 'Perseverance Technology'
release = '4.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel"
]

templates_path = ['_templates']

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    "analytics_anonymize_ip": False,
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
    "globaltoc_collapse": True,
    "globaltoc_maxdepth": None,
}

source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autoclass_content = 'both'
autodoc_mock_imports = ["Moildev", "cv2", "numpy", "warning", 'dll']

html_show_sourcelink = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'MyProject'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'extraclassoptions': 'openany, oneside',
    'classoptions': ',openany'
}


latex_logo = 'assets/logo.jpg'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Moildev.tex', 'Moildev Documentation',
     'Haryanto', 'manual'),
]

autodoc_default_flags = ['members', 'inherited-members']
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'undoc-members': True,
    'show-inheritance': True}

autosummary_generate = True

add_module_names = False

# -- Options for manual page output ------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'Moildev', 'Moildev Documentation',
     [author], 1)
]

# -- Options for Epub output -------------------------------------------------
epub_title = project

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

try:
    html_context
except NameError:
    html_context = dict()
html_context['display_lower_left'] = True

if 'REPO_NAME' in os.environ:
    REPO_NAME = os.environ['REPO_NAME']
else:
    REPO_NAME = ''

# SET CURRENT_LANGUAGE
if 'current_language' in os.environ:
    # get the current_language env var set by buildDocs.sh
    current_language = os.environ['current_language']
else:
    # set this build's current language to english
    current_language = 'en'

# tell the theme which language to we're currently building
html_context['current_language'] = current_language

repo = Repo(search_parent_directories=True)

if 'current_version' in os.environ:
    # get the current_version env var set by buildDocs.sh
    current_version = os.environ['current_version']
else:
    # set this build's current version by looking at the branch
    current_version = repo.active_branch.name

# tell the theme which version we're currently on ('current_version' affects
# the lower-left rtd menu and 'version' affects the logo-area version)
html_context['current_version'] = current_version
html_context['version'] = current_version

html_context['languages'] = [('en', '/' + REPO_NAME + '/en/' + current_version + '/')]

languages = [lang.name for lang in os.scandir('locales') if lang.is_dir()]
for lang in languages:
    html_context['languages'].append((lang, '/' + REPO_NAME + '/' + lang + '/' + current_version + '/'))


html_context['versions'] = list()

versions = [branch.name for branch in repo.branches]
for version in versions:
    html_context['versions'].append((version, '/' + REPO_NAME + '/' + current_language + '/' + version + '/'))

rinoh_documents = [(
    master_doc,
    'target',
    project + ' Documentation',
    '© ' + copyright,
)]
today_fmt = "%B %d, %Y"

# settings for EPUB
epub_basename = 'target'
html_context['downloads'] = list()
html_context['downloads'].append(('pdf',
                                  '/' + REPO_NAME + '/' + current_language + '/' + current_version +
                                  '/' + project + '-docs_' + current_language + '_' + current_version + '.pdf'))

html_context['downloads'].append(('epub',
                                  '/' + REPO_NAME + '/' + current_language + '/' + current_version +
                                  '/' + project + '-docs_' + current_language + '_' + current_version + '.epub'))

# for GitHub pages // need to change when use in another project
html_context['display_github'] = True
html_context['github_user'] = 'perseverance-tech-tw'
html_context['github_repo'] = 'moildev'
html_context['github_version'] = f'{current_version}/docs/'
