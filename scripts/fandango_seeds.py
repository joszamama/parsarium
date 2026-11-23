"""Seed AFL++ and native-engine runs from a target's default Fandango route.

`afl prepare --fandango N` and `native prepare --fandango N` call
`generate_seeds`, which runs `fandango_generate` into RUN_DIR/fandango with no
bridges. `fandango generate --prepare-afl` passes its existing receipt with
`--fandango-receipt`. Either way the plan's `seed_generation` field records
the generator version, spec, spec hash, random seed and counts, and every
generated file is checked against the receipt's output hashes before it is
copied into the seeds. The control is always added by the prepare script.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from run_case import ROOT


DEFAULT_RANDOM_SEED = 42
RECEIPT_DIRECTORY = "fandango"


def add_arguments(cli: argparse.ArgumentParser) -> None:
    """Options shared by prepare_afl_run.py and prepare_native_run.py."""
    group = cli.add_mutually_exclusive_group()
    group.add_argument("--fandango", type=int, metavar="N",
                       help="generate N valid seeds with the target's default Fandango route "
                            "into RUN_DIR/fandango (the control is always kept)")
    group.add_argument("--fandango-receipt", type=Path, metavar="FANDANGO_JSON",
                       help="add the files of an existing fandango generate receipt")
    cli.add_argument("--fandango-seed", type=int, default=DEFAULT_RANDOM_SEED, metavar="S",
                     help=f"Fandango --random-seed with --fandango (default {DEFAULT_RANDOM_SEED})")


def check_arguments(cli: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.fandango is not None and not 1 <= args.fandango <= 10000:
        cli.error("--fandango must be between 1 and 10000")
    if args.fandango_seed < 0:
        cli.error("--fandango-seed must be non-negative")
    if args.fandango_receipt is not None and not args.fandango_receipt.is_file():
        cli.error(f"Fandango receipt does not exist: {args.fandango_receipt}")


def portable(value: str, run_dir: Path) -> str:
    """Write the run directory as $RUN_DIR and the repository as $PARSARIUM_HOME."""
    return (value.replace(str(run_dir), "$RUN_DIR")
                 .replace(str(ROOT), "$PARSARIUM_HOME"))


def spec_name(spec: dict) -> str:
    name = spec["name"]
    if spec.get("kind") == "file":
        path = Path(name)
        if path.is_absolute() and path.resolve().is_relative_to(ROOT):
            return path.resolve().relative_to(ROOT).as_posix()
    return name


def provenance(receipt_path: Path, run_dir: Path, project: str) -> tuple[Path, list[Path], dict]:
    """Check a fandango.json receipt and return its corpus, files and plan record."""
    receipt_path = receipt_path.resolve()
    receipt = json.loads(receipt_path.read_text())
    if receipt.get("project") != project:
        raise ValueError(f"Fandango receipt is for {receipt.get('project')}, not {project}")
    if receipt.get("exit_code") != 0 or receipt.get("problems"):
        raise ValueError(f"Fandango receipt records a failed generation: {receipt_path}")
    corpus = receipt_path.parent / "generated"
    files = []
    for output in receipt.get("outputs") or []:
        path = (corpus / output["path"]).resolve()
        if not path.is_relative_to(corpus.resolve()) or not path.is_file() or path.is_symlink():
            raise ValueError(f"generated file is missing: {output['path']}")
        if sha256(path.read_bytes()).hexdigest() != output["sha256"]:
            raise ValueError(f"generated file changed after generation: {output['path']}")
        files.append(path)
    if not files:
        raise ValueError(f"Fandango receipt lists no generated files: {receipt_path}")
    spec = receipt["spec"]
    location = (receipt_path.relative_to(run_dir).as_posix()
                if receipt_path.is_relative_to(run_dir) else portable(str(receipt_path), run_dir))
    record = {
        "generator": "Fandango",
        "generator_version": receipt["fandango"]["version"],
        "spec_kind": spec["kind"],
        "spec": spec_name(spec),
        "spec_sha256": spec["sha256"],
        "random_seed": receipt["seed"],
        "requested_count": receipt["requested_count"],
        "output_count": receipt["output_count"],
        "unique_outputs": receipt["unique_outputs"],
        "generator_command": [portable(part, run_dir) for part in receipt["command"]],
        "receipt": location,
    }
    return corpus, files, record


def generate_seeds(fmt: str, ecosystem: str, slug: str, run_dir: Path,
                   count: int, random_seed: int) -> Path:
    """Run the default Fandango route into RUN_DIR/fandango and return its receipt."""
    import fandango_generate

    destination = run_dir / RECEIPT_DIRECTORY
    argv = [fmt, ecosystem, slug, str(destination), "--count", str(count),
            "--seed", str(random_seed)]
    try:
        code = fandango_generate.main(argv)
    except SystemExit as error:
        code = error.code
    receipt = destination / "fandango.json"
    if code:
        detail = f"; receipt: {receipt}" if receipt.is_file() else ""
        raise RuntimeError(f"Fandango seed generation failed with exit code {code}{detail}")
    return receipt
