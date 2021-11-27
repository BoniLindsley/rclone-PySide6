#!/usr/bin/env python3

# # Sphinx configuration file

import pathlib
import sys

# Let documentation source code find source code of this package.
script_path = pathlib.Path(__file__).absolute()
sys.path.insert(0, str(script_path.parent.parent / "src"))

# ## Project information

project = "rclone-PySide6"
"""The documented project’s name."""

author = "Boni Lindsley"
"""
The author name(s) of the document.

The default value is 'unknown'.
"""

copyright = "Boni Lindsley"
"""A copyright statement in the style '2008, Author Name'."""

# ## General configuration

extensions = [
    "recommonmark",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]
"""
A list of strings that are module names of extensions.

These can be extensions coming with Sphinx (named sphinx.ext.*)
or custom ones.
Note that you can extend `sys.path` within the conf file
if your extensions live in another directory -
but make sure you use absolute paths.
If your extension path is relative to the configuration directory,
use `os.path.abspath()`.
The configuration file itself can be an extension;
for that, you only need to provide a `setup()` function in it.
"""

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
"""
The file extensions of source files.

Sphinx considers the files with this suffix as sources.
The value can be a dictionary mapping file extensions to file types.
File extensions have to start with a dot (e.g. .rst).
Default is {'.rst': 'restructuredtext'}.
So, by default, Sphinx only supports 'restructuredtext' file type.

The value may also be a list of file extensions.
Sphinx will consider that all to be 'restructuredtext' file type.

* Changed in version 1.3: Can now be a list of extensions.
* Changed in version 1.8: Support file type mapping
"""

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
"""
A list of glob-style patterns that should be excluded
when looking for source files.

They are matched against the source file names
relative to the source directory,
using slashes as directory separators on all platforms.
They are also consulted when looking for static files
in `html_static_path` and `html_extra_path`.

* New in version 1.0.
"""

# ## Extension: sphinx.ext.autodoc

autoclass_content = "class"
"""
This value selects what content will be inserted
into the main body of an autoclass directive.

The possible values are:

  * 'class': Only the class’ docstring is inserted.
      This is the default.
      You can still document `__init__` as a separate method
      using automethod or the members option to autoclass.
  * 'both': Both the class’ and the `__init__` method’s docstring
      are concatenated and inserted.
  * 'init': Only the `__init__` method’s docstring is inserted.

New in version 0.3.

If the class has no `__init__` method
or if the `__init__` method’s docstring is empty,
but the class has a `__new__` method’s docstring, it is used instead.

New in version 1.4.
"""

autodoc_default_options = {
    # Do not show these members.
    # Note that documentation for `__init__` can still be added
    # by setting `autoclass_content` to `both` or `init`.
    "exclude-members": "__dict__, __module__, __weakref__",
    # Add all documented members. Boolean or 'var1, var2'.
    "members": True,
    # Add dunder members.
    "special-members": True,
    # Insert list of base classes.
    "show-inheritance": True,
    # Include undocumented members
    "undoc-members": True,
    #'ignore-module-all',
    #'imported-members',
    #'inherited-members',
    #'member-order',
    #'private-members',
}

autodoc_inherit_docstrings = False

autodoc_typehints = "description"
"""
How to represents typehints.

The setting takes the following values:

-   'signature': Show typehints as its signature (default)
-   'description': Show typehints as content of function or method
-   'none': Do not show typehints

New in version 2.1.

New in version 3.0: New option 'description' is added.
"""

# ## Extension: sphinx.ext.intersphinx

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
"""
The locations and names of other projects
that should be linked to in this documentation.

A dictionary mapping unique identifiers
to a tuple `(target, inventory)`.
Each target is the base URI of a foreign Sphinx documentation set
and can be a local path or an HTTP URI.
The `inventory` indicates where the inventory file can be found:
it can be `None` (at the same location as the base URI)
or another local or HTTP URI.

The unique identifier can be used to prefix cross-reference targets,
so that it is clear which intersphinx set the target belongs to.
A link like :ref:`comparison manual <python:comparisons>`
will link to the label “comparisons” in the doc set “python”,
if it exists.

Relative local paths for target locations are taken
as relative to the base of the built documentation,
while relative local paths for inventory locations are taken
as relative to the source directory.

When fetching remote inventory files,
proxy settings will be read
from the `$HTTP_PROXY` environment variable.
"""
