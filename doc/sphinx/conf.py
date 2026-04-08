"""Sphinx configuration"""

# pylint: disable=invalid-name

# -- Imports ------------------------------------------------------------------

from pathlib import Path
from datetime import datetime

from sphinx_pyproject import SphinxConfig

# -- Project information ------------------------------------------------------

config = SphinxConfig(
    Path(__file__).parent.parent.parent / "pyproject.toml", globalns=globals()
)
# pylint: disable=redefined-builtin,undefined-variable
copyright = f"{datetime.now().year}, {author}"  # type: ignore[name-defined]
# pylint: enable=redefined-builtin
project = name  # type: ignore[name-defined]
# pylint: enable=undefined-variable

# -- General configuration ----------------------------------------------------

extensions = [
    "myst_parser",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- HTML Theme ---------------------------------------------------------------

html_theme = "sphinx_rtd_theme"

# pylint: enable=invalid-name
