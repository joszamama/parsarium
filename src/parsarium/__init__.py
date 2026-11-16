"""Parsarium: an open testbed of real parsers.

The package installs the ``parsarium`` command and a small Python API. The
harnesses, controls, and catalog data live in a versioned snapshot that is
downloaded and checked on first use. See https://parsarium.com.
"""

__version__ = "2026.11.16"

from .snapshot import home  # noqa: E402

__all__ = ["__version__", "home"]
