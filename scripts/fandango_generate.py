"""Generate inputs with Fandango for one verified project and record provenance.

Example:
  python3 scripts/fandango_generate.py png c lodepng runs/png-lodepng-fandango \\
    --fanbase png --count 100 --seed 42 --prepare-afl

The output directory holds generated/ (Fandango's -d target), fandango.json
(the receipt), and optionally replay/ and afl/. AFL++ is prepared, never
started. `parsarium.py fandango setup` installs a pinned managed version.
"""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import time
import venv

from run_case import MAX_CASE_BYTES, ROOT, project_for
from format_registry import ECOSYSTEMS, PROJECT_FORMATS
from mp3_plain import BUNDLED_DECODED_SHA256, SOURCE_CONTROLS, validate_frames


FORMATS = PROJECT_FORMATS
# Target format -> Fanbase format directory. Formats missing here have no
# Fanbase spec as of index.yml schema 2 and need --spec. MP3 is resolved per
# target (tagged_mp3_target): targets verified on the ID3v2-tagged control use
# Fanbase's mp3 grammar; targets verified on untagged Layer III frames use the
# local plain grammar, because Fanbase's mp3 grammar emits ID3 tags plus
# Layer I/II frames and removing the tags does not yield a contiguous Layer III
# stream.
# Fanbase has no YAML spec, so yaml uses the bundled schema-neutral yaml.fan.
# Fanbase has no TOML spec either; toml uses the local toml.fan.
FANBASE_FORMATS = {"png": "png", "zip": "zip", "wav": "wav", "svg": "svg",
                   "json": "json", "xml": "xml"}
TAGGED_MP3_CONTROL_PREFIX = "controls/mp3/id3v2-tagged-"
LOCAL_SPECS = {"mp4": "mp4.fan", "pdf": "pdf.fan", "mp3": "mp3_plain.fan",
               "http11": "http11_request.fan", "ascii_ply": "ascii_ply.fan",
               "ascii_pnm": "ascii_pnm_p3.fan", "yaml": "yaml.fan", "toml": "toml.fan"}
# Passed as -x with --spec; Fandango defaults to '.txt' for -f.
EXTENSIONS = {"png": ".png", "zip": ".zip", "mp4": ".mp4", "wav": ".wav",
              "pdf": ".pdf", "svg": ".svg", "http11": ".http", "ascii_ply": ".ply",
              "ascii_pnm": ".pnm", "json": ".json",
              "xml": ".xml", "mp3": ".mp3", "yaml": ".yaml", "toml": ".toml"}
MINIMUM_VERSION = (1, 3)
SPEC_NAME = re.compile(r"[a-z0-9][a-z0-9-]*")
SLUG = re.compile(r"[a-z0-9][a-z0-9_-]*")
OUTPUT_ROOTS = (ROOT / "runs", ROOT / "generated")
DEFAULT_REGISTRY = "https://github.com/fandango-fuzzer/fanbase"
MANAGED_VERSION = "1.3.1"
MANAGED_LOCK = ROOT / "fuzzing" / "fandango" / "requirements.lock"
MANAGED_VENV = ROOT / ".venv" / "fandango-1.3.1-locked"
MANAGED_EXE = MANAGED_VENV / "bin" / "fandango"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def file_record(path: Path, base: Path) -> dict:
    checksum = sha256()
    size = 0
    with path.open("rb") as source:
        while chunk := source.read(1 << 16):
            checksum.update(chunk)
            size += len(chunk)
    return {"path": str(path.relative_to(base)), "sha256": checksum.hexdigest(),
            "bytes": size}


def output_directory(path: Path) -> Path:
    """Resolve the run directory; inside the repository only ignored roots are allowed."""
    resolved = path.expanduser().resolve()
    if resolved.is_relative_to(ROOT) and not any(
            resolved != root and resolved.is_relative_to(root) for root in OUTPUT_ROOTS):
        raise ValueError("output directory inside the repository must be below runs/ or generated/")
    if resolved.exists() and (not resolved.is_dir() or any(resolved.iterdir())):
        raise ValueError(f"output directory must be new or empty: {resolved}")
    return resolved


def fandango_executable(value: str | None) -> Path:
    found = shutil.which(value) if value else (
        str(MANAGED_EXE) if MANAGED_EXE.is_file() else shutil.which("fandango"))
    if not found:
        raise ValueError("fandango executable not found; run python3 parsarium.py fandango setup or pass --fandango PATH")
    return Path(found).resolve()


def setup() -> int:
    """Install the pinned generator in the ignored local .venv directory."""
    if MANAGED_EXE.is_file():
        version = fandango_version(MANAGED_EXE)
        if f"{MANAGED_VERSION}" in version:
            receipt_path = MANAGED_VENV / "setup.json"
            if not receipt_path.is_file():
                record_managed_setup(version)
            else:
                saved = json.loads(receipt_path.read_text())
                if (saved.get("executable_sha256") != digest(MANAGED_EXE)
                        or saved.get("fandango_version") != version
                        or saved.get("requirements_sha256") != digest(MANAGED_LOCK)
                        or saved.get("installed_packages") != managed_packages()):
                    raise RuntimeError("managed Fandango environment changed; remove its venv and rerun setup")
            print(f"Ready: {MANAGED_EXE} ({version})")
            return 0
        raise RuntimeError(f"unexpected Fandango in {MANAGED_VENV}: {version}")
    MANAGED_VENV.parent.mkdir(parents=True, exist_ok=True)
    venv.EnvBuilder(with_pip=True).create(MANAGED_VENV)
    python = MANAGED_VENV / "bin" / "python"
    subprocess.run([str(python), "-m", "pip", "install", "--disable-pip-version-check",
                    "--no-input", "--require-hashes", "-r", str(MANAGED_LOCK)], check=True)
    version = fandango_version(MANAGED_EXE)
    if MANAGED_VERSION not in version:
        raise RuntimeError(f"installed Fandango did not match {MANAGED_VERSION}: {version}")
    record_managed_setup(version)
    print(f"Ready: {MANAGED_EXE} ({version})")
    return 0


def record_managed_setup(version: str) -> None:
    receipt = {"schema_version": 1, "fandango_version": version,
               "executable_sha256": digest(MANAGED_EXE), "python": sys.version,
               "requirements_sha256": digest(MANAGED_LOCK),
               "installed_packages": managed_packages()}
    (MANAGED_VENV / "setup.json").write_text(json.dumps(receipt, indent=2) + "\n")


def managed_packages() -> list[str]:
    python = MANAGED_VENV / "bin" / "python"
    freeze = subprocess.run([str(python), "-m", "pip", "freeze"], check=True,
                            capture_output=True, text=True).stdout
    return freeze.splitlines()


def fandango_version(executable: Path) -> str:
    result = subprocess.run([str(executable), "--version"], capture_output=True,
                            text=True, timeout=120)
    text = (result.stdout + result.stderr).strip()
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    if result.returncode or not match:
        raise RuntimeError(f"could not read Fandango version: {text[-400:]!r}")
    if (int(match[1]), int(match[2])) < MINIMUM_VERSION:
        raise RuntimeError(f"Fandango {match[0]} is older than 1.3; Fanbase -F requires 1.3+")
    return text


def registry_entry(index: Path, name: str) -> dict | None:
    """Read one spec's path and sha256 from a Fanbase index.yml without PyYAML."""
    match = re.search(rf"^  kind: {re.escape(name)}\n  path: (\S+)\n  sha256: ([0-9a-f]{{64}})$",
                      index.read_text(), re.M)
    return {"path": match[1], "sha256": match[2]} if match else None


def registry_record(registry: Path | None, name: str) -> dict:
    if registry is None:
        return {"source": DEFAULT_REGISTRY, "pinned": False,
                "note": "Fandango resolves the default registry at run time; "
                        "the installed spec snapshot is the record"}
    index = registry / "index.yml"
    record = {"source": str(registry), "pinned": True,
              "index_sha256": digest(index), "entry": registry_entry(index, name)}
    if (registry / ".git").exists():
        head = subprocess.run(["git", "-C", str(registry), "rev-parse", "HEAD"],
                              capture_output=True, text=True)
        dirty = subprocess.run(["git", "-C", str(registry), "status", "--porcelain"],
                               capture_output=True, text=True)
        record["git_head"] = head.stdout.strip() or None
        record["git_dirty"] = bool(dirty.stdout.strip())
    return record


def build_command(executable: Path, args: argparse.Namespace, generated: Path,
                  spec: Path | None) -> list[str]:
    command = [str(executable), "fuzz"]
    if args.fanbase:
        command += ["-F", args.fanbase]
    else:
        command += ["-f", str(spec), "-x", EXTENSIONS[args.format]]
    command += ["-n", str(args.count), "-d", str(generated)]
    if args.seed is not None:
        command += ["--random-seed", str(args.seed)]
    return command


def tagged_mp3_target(ecosystem: str, slug: str) -> bool:
    """True for an MP3 target verified on the ID3v2-tagged control."""
    manifest = ROOT / "projects" / "mp3" / ecosystem / slug / "manifest.json"
    return (manifest.is_file() and
            json.loads(manifest.read_text())["control"].startswith(TAGGED_MP3_CONTROL_PREFIX))


def fanbase_format(args: argparse.Namespace) -> str | None:
    if args.format == "mp3" and not args.fanbase:
        return "mp3" if tagged_mp3_target(args.ecosystem, args.slug) else None
    return FANBASE_FORMATS.get(args.format)


def validate(cli: argparse.ArgumentParser, args: argparse.Namespace) -> Path | None:
    if not SLUG.fullmatch(args.slug):
        cli.error("slug must be a project directory name such as lodepng")
    if not 1 <= args.count <= 10000:
        cli.error("--count must be between 1 and 10000")
    if args.seed is not None and args.seed < 0:
        cli.error("--seed must be non-negative")
    if args.timeout < 1:
        cli.error("--timeout must be positive")
    expected_fanbase = fanbase_format(args)
    if args.fanbase is None and args.spec is None:
        if expected_fanbase is not None:
            args.fanbase = expected_fanbase
        elif args.format in LOCAL_SPECS:
            args.spec = ROOT / "fuzzing/fandango/specs" / LOCAL_SPECS[args.format]
        else:
            cli.error(f"no bundled {args.format} spec; pass --spec FILE.fan")
    if args.fanbase:
        expected = expected_fanbase
        if expected is None:
            cli.error(f"Fanbase has no {args.format} spec; pass --spec FILE.fan")
        if not SPEC_NAME.fullmatch(args.fanbase) or not (
                args.fanbase == expected or args.fanbase.startswith(expected + "-")):
            cli.error(f"--fanbase must name a {expected} spec, such as '{expected}' or '{expected}-boundary'")
        if args.fanbase_registry and not (args.fanbase_registry / "index.yml").is_file():
            cli.error("--fanbase-registry must be a local Fanbase checkout containing index.yml")
        return None
    if args.fanbase_registry:
        cli.error("--fanbase-registry applies only to --fanbase")
    spec = args.spec.expanduser().resolve()
    if spec.suffix != ".fan" or not spec.is_file():
        cli.error("--spec must be an existing .fan file")
    return spec


def bridge_commands(args: argparse.Namespace, run_dir: Path, receipt: dict) -> list[tuple[str, list[str]]]:
    generated = str(run_dir / "generated")
    steps = []
    if args.replay:
        spec = receipt["spec"]
        steps.append(("replay", [
            sys.executable, str(ROOT / "scripts/replay_corpus.py"),
            args.format, args.ecosystem, args.slug, generated, str(run_dir / "replay"),
            "--generator", "Fandango", "--generator-version", receipt["fandango"]["version"],
            "--spec", spec["name"], "--spec-sha256", spec["sha256"],
            "--generator-command", shlex.join(receipt["command"])]))
    if args.prepare_afl:
        steps.append(("afl_prepare", [
            sys.executable, str(ROOT / "scripts/prepare_afl_run.py"),
            args.format, args.ecosystem, args.slug, str(run_dir / "afl"),
            "--seed-dir", generated]))
    return steps


def write_receipt(run_dir: Path, receipt: dict) -> None:
    (run_dir / "fandango.json").write_text(json.dumps(receipt, indent=2) + "\n")


def add_arguments(cli: argparse.ArgumentParser) -> None:
    cli.add_argument("format", choices=FORMATS)
    cli.add_argument("ecosystem", choices=ECOSYSTEMS)
    cli.add_argument("slug")
    cli.add_argument("run_dir", type=Path)
    source = cli.add_mutually_exclusive_group()
    source.add_argument("--fanbase", metavar="NAME", help="Fanbase spec name, passed as fandango fuzz -F")
    source.add_argument("--spec", type=Path, metavar="FILE.fan", help="local spec, passed as fandango fuzz -f")
    cli.add_argument("--count", type=int, default=100, help="outputs to request (-n)")
    cli.add_argument("--seed", type=int, help="--random-seed and PYTHONHASHSEED")
    cli.add_argument("--fandango", help="Fandango executable (default: fandango on PATH)")
    cli.add_argument("--fanbase-registry", type=Path,
                     help="local Fanbase checkout to pin, exported as FANBASE_REGISTRY")
    cli.add_argument("--timeout", type=int, default=3600, help="seconds before Fandango is stopped")
    cli.add_argument("--replay", action="store_true", help="replay the corpus through the project")
    cli.add_argument("--prepare-afl", action="store_true",
                     help="prepare (not start) an AFL++ run seeded with the corpus")


def generate(cli: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    spec = validate(cli, args)
    project, manifest = project_for(args.format, args.ecosystem, args.slug)
    if args.prepare_afl:
        overlay = ROOT / "fuzzing/afl-native" / args.format / args.ecosystem / args.slug
        overlay_receipt = overlay / "verification.json"
        if not overlay_receipt.is_file() or not json.loads(overlay_receipt.read_text()).get("pass"):
            cli.error("AFL++ overlay is not verified; run python3 parsarium.py afl build FORMAT ECOSYSTEM SLUG")
    run_dir = output_directory(args.run_dir)
    if spec is not None and spec.is_relative_to(run_dir):
        cli.error("--spec must be outside the output directory")
    executable = fandango_executable(args.fandango)
    version = fandango_version(executable)
    bundled_plain_mp3 = (args.format == "mp3" and
                         spec == ROOT / "fuzzing/fandango/specs/mp3_plain.fan")
    if bundled_plain_mp3:
        for path, expected in SOURCE_CONTROLS.items():
            if digest(ROOT / path) != expected:
                raise ValueError(f"bundled MP3 source control changed: {path}")

    generated = run_dir / "generated"
    spec_home = run_dir / "fanbase-specs"
    generated.mkdir(parents=True)
    env = dict(os.environ)
    overrides = {}
    if args.fanbase:
        # An empty first FANDANGO_PATH entry makes Fandango install a fresh copy
        # of the -F spec here, which becomes the run's spec snapshot.
        spec_home.mkdir()
        overrides["FANDANGO_PATH"] = str(spec_home)
        if args.fanbase_registry:
            overrides["FANBASE_REGISTRY"] = str(args.fanbase_registry.expanduser().resolve())
    if args.seed is not None:
        overrides["PYTHONHASHSEED"] = str(args.seed)
    if executable == MANAGED_EXE.resolve() and "SSL_CERT_FILE" not in env:
        # Framework Python on macOS can lack a system OpenSSL CA path. pip's
        # bundled CA store is part of the recorded managed installation.
        ca_path = subprocess.run(
            [str(MANAGED_VENV / "bin" / "python"), "-c",
             "import pip._vendor.certifi as certifi; print(certifi.where())"],
            check=True, capture_output=True, text=True).stdout.strip()
        if Path(ca_path).is_file():
            overrides["SSL_CERT_FILE"] = ca_path
    env.update(overrides)
    spec_before = digest(spec) if spec else None
    if spec:
        shutil.copy2(spec, run_dir / ("spec-" + spec.name))
    command = build_command(executable, args, generated, spec)
    project_receipt = project / ("control-verification.json" if
        manifest.get("coverage_kind") == "native_source_afl_feedback" else "verification.json")
    receipt = {
        "schema_version": 1,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(project.relative_to(ROOT / "projects")),
        "package": manifest["package"],
        "release": manifest.get("release", manifest.get("runtime")),
        "source_sha256": manifest["source_sha256"],
        "project_receipt_sha256": digest(project_receipt),
        "fandango": {"executable": str(executable), "executable_sha256": digest(executable),
                     "version": version},
        "command": command, "environment": overrides, "cwd": str(run_dir),
        "seed": args.seed, "requested_count": args.count,
    }
    managed_setup = MANAGED_VENV / "setup.json"
    if executable == MANAGED_EXE.resolve() and managed_setup.is_file():
        setup_record = json.loads(managed_setup.read_text())
        if (setup_record.get("executable_sha256") != digest(executable)
                or setup_record.get("fandango_version") != version
                or setup_record.get("requirements_sha256") != digest(MANAGED_LOCK)
                or setup_record.get("installed_packages") != managed_packages()):
            raise RuntimeError("managed Fandango setup receipt changed; rerun setup")
        receipt["fandango"]["managed_setup_sha256"] = digest(managed_setup)
        receipt["fandango"]["requirements_sha256"] = setup_record["requirements_sha256"]
        receipt["fandango"]["installed_packages"] = setup_record["installed_packages"]
    if "SSL_CERT_FILE" in overrides:
        receipt["ssl_cert_file_sha256"] = digest(Path(overrides["SSL_CERT_FILE"]))
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=run_dir, env=env, capture_output=True,
                                text=True, errors="replace", timeout=args.timeout)
        receipt["exit_code"] = result.returncode
        receipt["stdout_tail"] = result.stdout[-4000:]
        receipt["stderr_tail"] = result.stderr[-4000:]
    except subprocess.TimeoutExpired:
        receipt["exit_code"] = None
        receipt["timed_out"] = True
    receipt["duration_seconds"] = round(time.monotonic() - started, 3)

    if args.fanbase:
        snapshots = sorted(spec_home.rglob(f"{args.fanbase}.fan"))
        metadata = sorted(spec_home.rglob(f"{args.fanbase}.yml"))
        registry = registry_record(
            args.fanbase_registry.expanduser().resolve() if args.fanbase_registry else None,
            args.fanbase)
        snapshot = file_record(snapshots[0], run_dir) if len(snapshots) == 1 else None
        entry = registry.get("entry")
        receipt["spec"] = {
            "kind": "fanbase", "name": args.fanbase, "registry": registry,
            "snapshot": snapshot,
            "metadata": file_record(metadata[0], run_dir) if len(metadata) == 1 else None,
            "sha256": snapshot["sha256"] if snapshot else None,
            "matches_registry_index": (snapshot["sha256"] == entry["sha256"]
                                       if snapshot and entry else None)}
    else:
        receipt["spec"] = {"kind": "file", "name": str(spec), "sha256": spec_before,
                           "copy": "spec-" + spec.name,
                           "unchanged_after_run": digest(spec) == spec_before,
                           "note": "files included by the spec are not hashed"}

    files = sorted(path for path in generated.rglob("*") if path.is_file() or path.is_symlink())
    links = [path for path in files if path.is_symlink()]
    files = [path for path in files if not path.is_symlink()]
    outputs = [file_record(path, generated) for path in files]
    receipt["outputs"] = outputs
    receipt["output_count"] = len(outputs)
    receipt["unique_outputs"] = len({item["sha256"] for item in outputs})
    receipt["output_bytes"] = sum(item["bytes"] for item in outputs)
    receipt["empty_outputs"] = sum(1 for item in outputs if not item["bytes"])
    receipt["over_limit_outputs"] = sum(1 for item in outputs if item["bytes"] > MAX_CASE_BYTES)
    receipt["symlinks_skipped"] = [str(path.relative_to(generated)) for path in links]
    receipt["input_limit_bytes"] = MAX_CASE_BYTES
    if args.format == "mp3" and not args.fanbase:
        receipt["plain_mp3_route"] = {
            "source": "local_spec", "postprocess": "none",
            "validation": "contiguous complete MPEG-1/2 Layer III frame headers",
            "limit_bytes": MAX_CASE_BYTES,
            "bundled_decoded_samples": bundled_plain_mp3,
            "validator_sha256": digest(ROOT / "scripts/mp3_plain.py"),
            "source_controls": SOURCE_CONTROLS if bundled_plain_mp3 else None,
        }

    problems = []
    if args.format == "mp3" and not args.fanbase:
        for path, record in zip(files, outputs):
            if record["bytes"] > MAX_CASE_BYTES:
                continue
            try:
                validation = validate_frames(path.read_bytes())
                bundled = receipt["plain_mp3_route"]["bundled_decoded_samples"]
                validation["pinned_go_and_rust_decode_checked"] = (
                    bundled and record["sha256"] in BUNDLED_DECODED_SHA256)
                record["format_validation"] = validation
                if bundled and not validation["pinned_go_and_rust_decode_checked"]:
                    problems.append(f"{record['path']}: bundled MP3 output differs from the six decoded samples")
            except ValueError as error:
                problems.append(f"{record['path']}: {error}")
    if receipt["exit_code"] != 0:
        problems.append("Fandango did not exit cleanly")
    if not outputs:
        problems.append("Fandango produced no files")
    if links:
        problems.append("Fandango output contains symlinks")
    if receipt["over_limit_outputs"] or receipt["empty_outputs"]:
        problems.append(f"outputs must be 1 to {MAX_CASE_BYTES} bytes for replay and AFL++ seeds")
    if args.fanbase and receipt["spec"]["snapshot"] is None:
        problems.append(f"no single installed {args.fanbase}.fan found under {spec_home}")
    if args.fanbase and receipt["spec"]["matches_registry_index"] is False:
        problems.append("installed Fanbase spec differs from the pinned registry index")
    if spec and not receipt["spec"]["unchanged_after_run"]:
        problems.append("--spec changed while Fandango ran")
    receipt["problems"] = problems
    receipt["bridges"] = []
    write_receipt(run_dir, receipt)
    print(f"{len(outputs)} of {args.count} requested outputs in {generated}")
    if outputs and len(outputs) != args.count:
        print(f"note: Fandango wrote {len(outputs)} files, not {args.count}", file=sys.stderr)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        print(f"receipt: {run_dir / 'fandango.json'}", file=sys.stderr)
        return 1

    for name, step in bridge_commands(args, run_dir, receipt):
        print(f"{name}: {shlex.join(step)}", flush=True)
        code = subprocess.call(step, cwd=ROOT)
        receipt["bridges"].append({"step": name, "command": step, "exit_code": code})
        write_receipt(run_dir, receipt)
        if code:
            print(f"error: {name} failed with exit code {code}", file=sys.stderr)
            return code
    if args.prepare_afl:
        print("AFL++ was prepared, not started. Next:")
        print(f"  python3 parsarium.py afl run {shlex.quote(str(run_dir / 'afl'))} --check")
    print(f"receipt: {run_dir / 'fandango.json'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    add_arguments(cli)
    return generate(cli, cli.parse_args(argv))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(f"fandango_generate: {error}") from error
