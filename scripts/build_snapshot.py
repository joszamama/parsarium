#!/usr/bin/env python3
"""Build the snapshot tarball that the ``parsarium`` package downloads.

The tarball holds the committed harnesses, controls, catalog data, adapters,
and helper scripts at one commit, under ``parsarium-<version>/``. It is built
from ``git archive`` with fixed metadata, so the same commit and version give
the same bytes and the same SHA-256.

    python3 scripts/build_snapshot.py --version 2026.11.16 --out dist-snapshot --write-package

``--write-package`` also places the verified snapshot inside the Python
package. The wheel can then work without access to this repository's releases.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/joszamama/parsarium"
PATHS = ["parsarium.py", "LICENSE", "README.md", "PROTOCOL.md", "adapters", "catalog", "controls",
         "data", "fuzzing", "projects", "scripts", "sources"]


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("--version", required=True)
    cli.add_argument("--ref", default="HEAD")
    cli.add_argument("--out", type=Path, default=ROOT / "dist-snapshot")
    cli.add_argument("--write-package", action="store_true",
                     help="record the snapshot's URL and SHA-256 in src/parsarium/_snapshot.json")
    args = cli.parse_args()

    commit = git("rev-parse", args.ref).decode().strip()
    mtime = int(git("show", "-s", "--format=%ct", commit).decode().strip())
    prefix = f"parsarium-{args.version}"
    name = f"parsarium-snapshot-{args.version}.tar.gz"
    archive = git("archive", "--format=tar", commit, "--", *PATHS)

    raw = io.BytesIO()
    with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=9) as gz, \
            tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as out, \
            tarfile.open(fileobj=io.BytesIO(archive), mode="r") as src:
        def normalise(info: tarfile.TarInfo, name: str) -> tarfile.TarInfo:
            info.name = name
            info.mtime = mtime
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.pax_headers = {}
            return info

        root_dir = tarfile.TarInfo(prefix)
        root_dir.type = tarfile.DIRTYPE
        root_dir.mode = 0o755
        out.addfile(normalise(root_dir, prefix))
        for member in src:
            if member.type == tarfile.XGLTYPE or member.name == "pax_global_header":
                continue
            data = src.extractfile(member) if member.isfile() else None
            out.addfile(normalise(member, f"{prefix}/{member.name.rstrip('/')}"), data)
        meta = json.dumps({"version": args.version, "commit": commit, "source": REPO},
                          indent=2).encode() + b"\n"
        info = normalise(tarfile.TarInfo(), f"{prefix}/parsarium-snapshot.json")
        info.size = len(meta)
        info.mode = 0o644
        out.addfile(info, io.BytesIO(meta))

    payload = raw.getvalue()
    digest = hashlib.sha256(payload).hexdigest()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / name).write_bytes(payload)
    record = {
        "version": args.version,
        "url": f"{REPO}/releases/download/v{args.version}/{name}",
        "sha256": digest,
        "bytes": len(payload),
        "commit": commit,
        "prefix": prefix,
        "bundle": "_snapshot.tar.gz" if args.write_package else None,
    }
    if args.write_package:
        package = ROOT / "src/parsarium"
        (package / "_snapshot.tar.gz").write_bytes(payload)
        (package / "_snapshot.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
