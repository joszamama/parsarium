"""Short, reader-facing names for the adoption metrics used in rankings.

Ranking tables and the website show these instead of a generic "Metric" column,
so a number always says what it counts and where it comes from.
"""

from __future__ import annotations

# Primary metric of each ecosystem's pilot cells (PROTOCOL.md).
PRIMARY_BY_ECOSYSTEM = {
    "c": "Debian installations (popcon)",
    "cpp": "Debian installations (popcon)",
    "go": "Imported by (pkg.go.dev)",
    "java": "Direct dependents (deps.dev)",
    "javascript": "npm downloads (last month)",
    "python": "PyPI downloads (last month)",
    "rust": "crates.io downloads (90 days)",
    "php": "Packagist downloads (all time)",
}

# Active-matrix C/C++ cells recorded other primary metrics before the pilots existed.
PRIMARY_BY_FIELD = {
    ("c", "install_on_request_365d"): "Homebrew installs (365 days)",
    ("cpp", "install_on_request_365d"): "Homebrew installs (365 days)",
    ("c", "stars"): "GitHub stars",
    ("cpp", "stars"): "GitHub stars",
}

SUPPLEMENTAL_BY_KIND = {
    "debian_source_installed": "Debian installations (popcon)",
    "github_source_stars": "GitHub stars",
}

SPANISH = {
    "Debian installations (popcon)": "instalaciones en Debian (popcon)",
    "Imported by (pkg.go.dev)": "importado por (pkg.go.dev)",
    "Direct dependents (deps.dev)": "dependientes directos (deps.dev)",
    "npm downloads (last month)": "descargas en npm (último mes)",
    "PyPI downloads (last month)": "descargas en PyPI (último mes)",
    "crates.io downloads (90 days)": "descargas en crates.io (90 días)",
    "Packagist downloads (all time)": "descargas en Packagist (totales)",
    "Homebrew installs (365 days)": "instalaciones en Homebrew (365 días)",
    "GitHub stars": "estrellas en GitHub",
}

GENERIC_HEADERS = {"metric", "value", "recorded adoption metric"}


def primary_label(ecosystem: str, field: str | None = None) -> str:
    return PRIMARY_BY_FIELD.get((ecosystem, field or ""), PRIMARY_BY_ECOSYSTEM[ecosystem])


# Hand-written pilot ranking tables use shorter headers for the same metrics.
_HEADER_ALIASES = {
    "installations": None, "source installations": None, "downloads": None,
    "last-month downloads": None, "stars": "GitHub stars", "github stars": "GitHub stars",
    "dev installs": "Debian development-package installations (popcon)",
    "dev package installs": "Debian development-package installations (popcon)",
}
SPANISH["Debian development-package installations (popcon)"] = "instalaciones del paquete de desarrollo en Debian (popcon)"


def normalize(ecosystem: str, header: str) -> str:
    """Map a table header to a reader-facing metric name for this ecosystem."""
    key = header.strip().casefold()
    if key in GENERIC_HEADERS or key in _HEADER_ALIASES and _HEADER_ALIASES[key] is None:
        return PRIMARY_BY_ECOSYSTEM[ecosystem]
    return _HEADER_ALIASES.get(key) or header
