"""Locate, download, and verify the Parsarium snapshot.

A snapshot is a tarball of the repository's harnesses, controls, catalog
data, and helper scripts at one release. Each package version names exactly
one snapshot by URL and SHA-256, so a version pins every target.

Resolution order:

1. ``PARSARIUM_HOME``: an existing checkout or unpacked snapshot. Nothing is
   downloaded. Use this when working from a clone of the repository.
2. The cache: ``PARSARIUM_CACHE`` or the platform cache directory, holding
   one unpacked snapshot per package version.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.request
from importlib import resources
from pathlib import Path

from . import __version__

ENTRY = "parsarium.py"


class SnapshotError(RuntimeError):
    """The snapshot is missing, cannot be downloaded, or does not verify."""


def snapshot_info() -> dict:
    """Return the snapshot this package version was released with."""
    data = json.loads(resources.files("parsarium").joinpath("_snapshot.json").read_text())
    if os.environ.get("PARSARIUM_SNAPSHOT_URL"):
        data["url"] = os.environ["PARSARIUM_SNAPSHOT_URL"]
        data["sha256"] = os.environ.get("PARSARIUM_SNAPSHOT_SHA256") or data.get("sha256")
    return data


def cache_root() -> Path:
    if os.environ.get("PARSARIUM_CACHE"):
        return Path(os.environ["PARSARIUM_CACHE"]).expanduser()
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "parsarium"
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "parsarium" / "Cache"
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "parsarium"


def home(fetch: bool = True, quiet: bool = False) -> Path:
    """Return the directory that holds ``parsarium.py`` and the targets.

    Downloads and verifies the snapshot on first use unless ``fetch`` is false.
    """
    override = os.environ.get("PARSARIUM_HOME")
    if override:
        path = Path(override).expanduser().resolve()
        if not (path / ENTRY).is_file():
            raise SnapshotError(f"PARSARIUM_HOME={path} does not contain {ENTRY}")
        return path
    info = snapshot_info()
    target = cache_root() / info.get("version", __version__)
    if (target / ENTRY).is_file():
        return target
    if not fetch:
        raise SnapshotError(f"no snapshot at {target}; run `parsarium home --fetch`")
    if not info.get("url") or not info.get("sha256"):
        raise SnapshotError(
            "this is a development install without a released snapshot; "
            "set PARSARIUM_HOME to a clone of https://github.com/joszamama/parsarium")
    _install(info, target, quiet)
    return target


def _download(url: str, destination: Path, size: int | None, quiet: bool) -> str:
    digest = hashlib.sha256()
    if "://" not in url:
        url = Path(url).expanduser().resolve().as_uri()
    request = urllib.request.Request(url, headers={"User-Agent": f"parsarium/{__version__}"})
    with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as out:
        total = size or int(response.headers.get("Content-Length") or 0)
        done = 0
        while chunk := response.read(1 << 20):
            out.write(chunk)
            digest.update(chunk)
            done += len(chunk)
            if not quiet and total and sys.stderr.isatty():
                print(f"\rparsarium: downloading snapshot {done / 2**20:5.1f}/{total / 2**20:.1f} MB",
                      end="", file=sys.stderr, flush=True)
    if not quiet:
        print(("\r" if sys.stderr.isatty() else "")
              + f"parsarium: downloaded snapshot ({done / 2**20:.1f} MB), checking SHA-256", file=sys.stderr)
    return digest.hexdigest()


def _safe_members(archive: tarfile.TarFile, prefix: str):
    for member in archive.getmembers():
        name = member.name
        if not (name == prefix or name.startswith(prefix + "/")):
            raise SnapshotError(f"unexpected path in snapshot: {name}")
        if name.startswith("/") or ".." in Path(name).parts:
            raise SnapshotError(f"unsafe path in snapshot: {name}")
        if member.issym() or member.islnk():
            link = Path(name).parent / member.linkname
            if member.linkname.startswith("/") or ".." in Path(os.path.normpath(link)).parts:
                raise SnapshotError(f"unsafe link in snapshot: {name}")
        if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
            raise SnapshotError(f"unsupported entry in snapshot: {name}")
        yield member


def _install(info: dict, target: Path, quiet: bool) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent, prefix=".download-") as work:
        work = Path(work)
        tarball = work / "snapshot.tar.gz"
        try:
            digest = _download(info["url"], tarball, info.get("bytes"), quiet)
        except OSError as error:
            raise SnapshotError(f"could not download {info['url']}: {error}") from error
        if digest != info["sha256"]:
            raise SnapshotError(f"snapshot checksum mismatch: expected {info['sha256']}, got {digest}")
        prefix = info.get("prefix", f"parsarium-{info.get('version', __version__)}")
        with tarfile.open(tarball) as archive:
            members = list(_safe_members(archive, prefix))
            if hasattr(tarfile, "data_filter"):
                archive.extractall(work, members=members, filter="data")
            else:  # Python 3.11 before 3.11.4
                archive.extractall(work, members=members)
        unpacked = work / prefix
        if not (unpacked / ENTRY).is_file():
            raise SnapshotError(f"snapshot does not contain {ENTRY}")
        if target.exists():  # another process finished first
            return
        try:
            unpacked.rename(target)
        except OSError:
            if not (target / ENTRY).is_file():
                raise
    if not quiet:
        print(f"parsarium: snapshot {info.get('version')} ready in {target}", file=sys.stderr)


def remove(version: str | None = None) -> Path:
    """Delete one cached snapshot (default: this package version's)."""
    target = cache_root() / (version or snapshot_info().get("version", __version__))
    if target.is_dir():
        shutil.rmtree(target)
    return target
