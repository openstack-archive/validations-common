#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

# Add the project
sys.path.insert(0, os.path.abspath('../..'))
# Add the extensions
sys.path.insert(0, os.path.join(os.path.abspath('.'), '_exts'))

# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinxcontrib.apidoc',
    'sphinxcontrib.rsvgconverter',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'openstackdocstheme',
    'ansible-autodoc'
]

# sphinxcontrib.apidoc options
apidoc_module_dir = '../../validations_common'
apidoc_output_dir = 'reference/api'
apidoc_excluded_paths = []
apidoc_separate_modules = True

# openstackdocstheme options
openstackdocs_repo_name = 'openstack/validations-common'
openstackdocs_use_storyboard = True
openstackdocs_pdf_link = True
openstackdocs_bug_project = 'tripleo'
openstackdocs_bug_tag = 'documentation'

# autodoc generation is a bit aggressive and a nuisance when doing heavy
# text edit cycles.
# execute "export SPHINX_DEBUG=1" in your terminal to disable
autodoc_mock_imports = ['validations_libs', 'oslotest']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
copyright = u'2021, OpenStack Foundation'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['validations_common.']

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'native'

# A list of glob-style patterns that should be excluded when looking for
# source files. They are matched against the source file names relative to the
# source directory, using slashes as directory separators on all platforms.
exclude_patterns = ['']

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
# html_theme_path = ["."]
# html_theme = '_theme'
# html_static_path = ['static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'validations-commondoc'
html_theme = 'openstackdocs'

latex_use_xindy = False

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    (
        'index',
        'doc-validations-common.tex',
        u'Validations Framework Client Documentation',
        u'OpenStack LLC',
        'manual'
    ),
]

# Allow deeper levels of nesting for \begin...\end stanzas
latex_elements = {'maxlistdepth': 10, 'extraclassoptions': ',openany,oneside'}
