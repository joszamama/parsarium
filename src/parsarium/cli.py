"""The ``parsarium`` command.

Package commands (``home``, ``run-selection``, ``--version``) are handled
here. Everything else is passed to the snapshot's own ``parsarium.py``, so the
installed command and a repository checkout behave the same way.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from . import __version__
from .snapshot import SnapshotError, cache_root, home, remove, snapshot_info
from . import selection

PACKAGE_HELP = f"""\
parsarium {__version__}: an open testbed of real parsers (https://parsarium.com)

usage: parsarium <command> [options]

Catalog and targets (from the snapshot):
  list, catalog, projects, show     browse verified parsers and runnable targets
  build, run, replay, run-format    build a target and run inputs through it
  observe FORMAT --corpus --results  record what each target read from each file
  afl ..., native ...               fuzz a target with AFL++ or its native engine
  fandango ...                      generate and replay format-aware inputs

Package commands:
  home [--fetch | --path | --remove]  show, extract, or delete the snapshot
  run-selection MANIFEST [options]    run a selection saved from parsarium.com/bench

Run `parsarium <command> --help` for details. The first command that needs
targets checks and extracts this version's bundled snapshot.
Running targets requires Docker.
"""


def _home_command(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="parsarium home", description="Show or manage the snapshot.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--fetch", action="store_true", help="extract and verify the bundled snapshot now")
    group.add_argument("--path", action="store_true", help="print only the snapshot directory")
    group.add_argument("--remove", action="store_true", help="delete this version's cached snapshot")
    args = parser.parse_args(argv)
    if args.remove:
        print(f"removed {remove()}")
        return 0
    info = snapshot_info()
    try:
        path = home(fetch=args.fetch)
    except SnapshotError as error:
        if args.path or args.fetch:
            raise
        print(f"package   {__version__}\nsnapshot  {info.get('version')} (not cached)\n"
              f"cache     {cache_root()}\nnote      {error}")
        return 0
    if args.path:
        print(path)
    else:
        print(f"package   {__version__}\nsnapshot  {info.get('version')}\n"
              f"commit    {info.get('commit') or '-'}\nhome      {path}")
    return 0


def _selection_command(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="parsarium run-selection",
        description="Run every target of a selection manifest saved from parsarium.com/bench.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--mode", choices=selection.MODES, default="control",
                        help="control files, your own files, a corpus, AFL++, or Fandango generation with replay (default: control)")
    parser.add_argument("--input", type=Path,
                        help="file or directory for --mode file/replay; with several formats, "
                             "one subdirectory per format (e.g. DIR/png/)")
    parser.add_argument("--out", type=Path, help="results directory (default: runs/<selection id>)")
    parser.add_argument("--seconds", type=int, default=3600, help="AFL++ budget per target")
    parser.add_argument("--count", type=int, default=100,
                        help="Fandango inputs per target (--mode fandango, and AFL++ seeds besides the control)")
    parser.add_argument("--seed", type=int, default=42, help="Fandango random seed")
    parser.add_argument("--dry-run", action="store_true", help="print the commands without running them")
    parser.add_argument("--allow-mismatch", action="store_true",
                        help="accept commit or target pin differences; print every difference")
    args = parser.parse_args(argv)
    return selection.run(args.manifest, home(), args.mode, args.input, args.out,
                         args.seconds, args.dry_run, args.allow_mismatch, args.count, args.seed)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if not argv or argv[0] in {"-h", "--help", "help"}:
            print(PACKAGE_HELP, end="")
            return 0
        if argv[0] in {"-V", "--version", "version"}:
            info = snapshot_info()
            print(f"parsarium {__version__} (snapshot {info.get('version')}, commit {info.get('commit') or '-'})")
            return 0
        if argv[0] == "home":
            return _home_command(argv[1:])
        if argv[0] == "run-selection":
            return _selection_command(argv[1:])
        root = home()
        return subprocess.call([sys.executable, str(root / "parsarium.py"), *argv])
    except (SnapshotError, ValueError, OSError) as error:
        print(f"parsarium: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
