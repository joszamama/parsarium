"""Browse verified parsers and launch their container harnesses."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
FORMATS = ("png", "zip", "mp4", "wav", "pdf", "svg", "http11",
           "ascii_ply", "ascii_pnm", "mp3_id3v2")
ECOSYSTEMS = ("c", "cpp", "go", "java", "javascript", "python", "rust", "php")


def json_file(path: Path):
    return json.loads(path.read_text())


def rows(format_name: str | None, ecosystem: str | None) -> list[dict]:
    cells = json_file(ROOT / "data/cells.json")["cells"]
    coverage = json_file(ROOT / "data/projects-coverage.json")["cells"]
    covered = {(item["format"], item["ecosystem"]): item for item in coverage}
    return [{"format": cell["format"], "ecosystem": cell["ecosystem"],
             "verified_third_party": cell["verified_third_party_count"],
             "verified_standard": cell["verified_standard_or_runtime_count"],
             "runnable": (covered[(cell["format"], cell["ecosystem"])]["containerized_verified"] +
                          covered[(cell["format"], cell["ecosystem"])]["standard_containerized_verified"]),
             "unresolved_leads": cell["unresolved_documentation_leads"]}
            for cell in cells
            if (not format_name or cell["format"] == format_name)
            and (not ecosystem or cell["ecosystem"] == ecosystem)]


def print_table(headers: tuple[str, ...], values: list[tuple]) -> None:
    widths = [max(len(header), *(len(str(row[index])) for row in values))
              for index, header in enumerate(headers)]
    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in values:
        print("  ".join(str(value).ljust(widths[index])
                        for index, value in enumerate(row)))


def catalog(format_name: str, ecosystem: str, as_json: bool) -> None:
    directory = ROOT / "data" / ecosystem / format_name
    if as_json:
        print(json.dumps({"cell": json_file(directory / "cell.json"),
                          "parsers": json_file(directory / "parsers.json")}, indent=2))
    else:
        print((directory / "ranking.md").read_text(), end="")


def projects(format_name: str | None, ecosystem: str | None, as_json: bool) -> None:
    entries = []
    for path in sorted((ROOT / "projects").glob("*/*/*/manifest.json")):
        manifest = json_file(path)
        if format_name and manifest["format"] != format_name:
            continue
        if ecosystem and manifest["ecosystem"] != ecosystem:
            continue
        entries.append({"format": manifest["format"],
                        "ecosystem": manifest["ecosystem"],
                        "slug": path.parent.name, "package": manifest["package"],
                        "release": manifest.get("release", manifest.get("runtime", "")),
                        "kind": manifest.get("kind", "third_party")})
    if as_json:
        print(json.dumps(entries, indent=2))
    else:
        print_table(("FORMAT", "ECOSYSTEM", "SLUG", "PACKAGE", "RELEASE"),
                    [(entry["format"], entry["ecosystem"], entry["slug"],
                      entry["package"], entry["release"]) for entry in entries])


def show(format_name: str, ecosystem: str, slug: str, as_json: bool) -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from run_case import project_for

    project, manifest = project_for(format_name, ecosystem, slug)
    info = {"project": str(project.relative_to(ROOT)),
            "package": manifest["package"],
            "release": manifest.get("release", manifest.get("runtime")),
            "kind": manifest.get("kind", "third_party"),
            "parser_api": manifest.get("api"), "control": manifest["control"],
            "fuzz_engine": manifest.get("fuzz_engine", "libFuzzer" if ecosystem in
                                        {"c", "cpp"} else None),
            "harness": str((project / manifest["harness"]).relative_to(ROOT)),
            "afl_overlay": str((ROOT / "fuzzing/afl-native" /
                                format_name / ecosystem / slug).relative_to(ROOT))}
    if manifest.get("catalog_parser"):
        parsers = json_file(ROOT / manifest["catalog_parser"])
        parser = next(item for item in parsers if item["name"] == manifest["package"])
        info["parser_api"] = parser.get("input_api")
        info["family"] = parser.get("family")
    if as_json:
        print(json.dumps(info, indent=2))
    else:
        for key, value in info.items():
            if value is not None:
                print(f"{key.replace('_', ' ')}: {value}")


def execute(script: str, *arguments: str) -> int:
    return subprocess.call([sys.executable, str(ROOT / "scripts" / script), *arguments], cwd=ROOT)


def build_afl(format_name: str, ecosystem: str, slug: str) -> int:
    sys.path.insert(0, str(ROOT / "scripts"))
    from run_case import image_for, project_for

    candidate = ROOT / "projects" / format_name / ecosystem / slug
    if (candidate / "manifest.json").is_file():
        candidate_manifest = json_file(candidate / "manifest.json")
        if candidate_manifest.get("coverage_kind") == "native_source_afl_feedback":
            return subprocess.call([sys.executable, str(ROOT / "fuzzing/afl-native" /
                format_name / ecosystem / slug / "verify-feedback.py")], cwd=ROOT)
    project, manifest = project_for(format_name, ecosystem, slug)
    _, image_id = image_for(project, manifest)
    verification = json_file(project / "verification.json")
    if image_id != verification["image_id"]:
        result = execute("run_project.py", format_name, ecosystem, slug)
        if result:
            return result
    custom = ROOT / "fuzzing" / "afl-native" / format_name / ecosystem / slug / "build.py"
    if custom.is_file():
        return subprocess.call([sys.executable, str(custom)], cwd=ROOT)
    if manifest.get("coverage_kind") == "native_binary_edges":
        return execute("build_afl_binary.py", format_name, ecosystem, slug)
    script = ("build_afl_native.py" if ecosystem in {"c", "cpp"} else
              "build_afl_rust.py" if ecosystem == "rust" else
              "build_afl_python.py" if ecosystem == "python" else
              "build_afl_bridge.py")
    return execute(script, format_name, ecosystem, slug)


def seed_arguments(args: argparse.Namespace) -> list[str]:
    result = []
    for path in args.seed:
        result += ["--seed", str(path)]
    for path in args.seed_dir:
        result += ["--seed-dir", str(path)]
    return result


def main() -> int:
    sys.path.insert(0, str(ROOT / "scripts"))
    import fandango_generate as generator

    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest="command", required=True)

    listed = commands.add_parser("list", help="show verified and runnable counts by format and ecosystem")
    listed.add_argument("--format", choices=FORMATS)
    listed.add_argument("--ecosystem", choices=ECOSYSTEMS)
    listed.add_argument("--json", action="store_true")

    cataloged = commands.add_parser("catalog", help="show one cell's verified ranking")
    cataloged.add_argument("format", choices=FORMATS)
    cataloged.add_argument("ecosystem", choices=ECOSYSTEMS)
    cataloged.add_argument("--json", action="store_true")

    project_list = commands.add_parser("projects", help="list containerized parsers")
    project_list.add_argument("--format", choices=FORMATS)
    project_list.add_argument("--ecosystem", choices=ECOSYSTEMS)
    project_list.add_argument("--json", action="store_true")

    shown = commands.add_parser("show", help="show one runnable parser")
    shown.add_argument("format", choices=FORMATS)
    shown.add_argument("ecosystem", choices=ECOSYSTEMS)
    shown.add_argument("slug")
    shown.add_argument("--json", action="store_true")

    built = commands.add_parser("build", help="build and verify one project container")
    built.add_argument("format", choices=FORMATS)
    built.add_argument("ecosystem", choices=ECOSYSTEMS)
    built.add_argument("slug")

    case = commands.add_parser("run", help="run one supplied input through a parser")
    case.add_argument("format", choices=FORMATS)
    case.add_argument("ecosystem", choices=ECOSYSTEMS)
    case.add_argument("slug")
    case.add_argument("file", type=Path)
    case.add_argument("--timeout", type=int, default=60)
    case.add_argument("--results", type=Path)

    corpus = commands.add_parser("replay", help="replay and preserve an external corpus")
    corpus.add_argument("format", choices=FORMATS)
    corpus.add_argument("ecosystem", choices=ECOSYSTEMS)
    corpus.add_argument("slug")
    corpus.add_argument("corpus", type=Path)
    corpus.add_argument("run_dir", type=Path)
    corpus.add_argument("--generator", default="external")
    corpus.add_argument("--generator-version")
    corpus.add_argument("--spec")
    corpus.add_argument("--spec-sha256")
    corpus.add_argument("--generator-command")
    corpus.add_argument("--per-case", action="store_true")
    corpus.add_argument("--workers", type=int, default=4)
    corpus.add_argument("--timeout", type=int, default=60)
    corpus.add_argument("--batch-timeout", type=int, default=3600)

    format_run = commands.add_parser("run-format", help="run every verified Docker harness for a format")
    format_run.add_argument("format", choices=FORMATS)
    format_run.add_argument("--ecosystem", choices=ECOSYSTEMS)
    format_run.add_argument("--file", type=Path)
    format_run.add_argument("--results", type=Path)
    format_run.add_argument("--workers", type=int, default=1)
    format_run.add_argument("--timeout", type=int, default=60)
    format_run.add_argument("--limit", type=int)
    format_run.add_argument("--list", action="store_true")

    afl = commands.add_parser("afl", help="build, prepare, run, and summarize AFL++")
    afl_commands = afl.add_subparsers(dest="action", required=True)
    afl_build = afl_commands.add_parser("build", help="build and verify one AFL++ overlay")
    afl_build.add_argument("format", choices=FORMATS)
    afl_build.add_argument("ecosystem", choices=ECOSYSTEMS)
    afl_build.add_argument("slug")
    afl_prepare = afl_commands.add_parser("prepare", help="copy seeds and pin an AFL++ run")
    afl_prepare.add_argument("format", choices=FORMATS)
    afl_prepare.add_argument("ecosystem", choices=ECOSYSTEMS)
    afl_prepare.add_argument("slug")
    afl_prepare.add_argument("run_dir", type=Path)
    afl_prepare.add_argument("--seed", type=Path, action="append", default=[])
    afl_prepare.add_argument("--seed-dir", type=Path, action="append", default=[])
    afl_prepare.add_argument("--timeout-ms", type=int)
    afl_run = afl_commands.add_parser("run", help="check or start a bounded AFL++ run")
    afl_run.add_argument("run_dir", type=Path)
    afl_run.add_argument("--seconds", type=int, default=3600)
    afl_run.add_argument("--check", action="store_true")
    afl_run.add_argument("--resume", action="store_true")
    afl_summary = afl_commands.add_parser("summary", help="summarize AFL++ statistics and saved files")
    afl_summary.add_argument("run_dir", type=Path)

    fandango = commands.add_parser("fandango", help="generate a corpus with Fandango and record provenance")
    fandango_commands = fandango.add_subparsers(dest="action", required=True)
    fandango_commands.add_parser("setup", help="install pinned Fandango in the ignored local .venv")
    fandango_generate = fandango_commands.add_parser(
        "generate", help="run fandango fuzz into a new run directory; optionally replay or prepare AFL++",
        description=generator.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    generator.add_arguments(fandango_generate)

    native = commands.add_parser("native", help="prepare and run ecosystem fuzz engines")
    native_commands = native.add_subparsers(dest="action", required=True)
    native_prepare = native_commands.add_parser("prepare", help="copy seeds and pin a native engine run")
    native_prepare.add_argument("format", choices=FORMATS)
    native_prepare.add_argument("ecosystem", choices=ECOSYSTEMS)
    native_prepare.add_argument("slug")
    native_prepare.add_argument("run_dir", type=Path)
    native_prepare.add_argument("--seed", type=Path, action="append", default=[])
    native_prepare.add_argument("--seed-dir", type=Path, action="append", default=[])
    native_prepare.add_argument("--duration-seconds", type=int, default=3600)
    native_run = native_commands.add_parser("run", help="check or start a native engine run")
    native_run.add_argument("run_dir", type=Path)
    native_run.add_argument("--check", action="store_true")

    args = cli.parse_args()
    if args.command == "list":
        items = rows(args.format, args.ecosystem)
        if args.json:
            print(json.dumps(items, indent=2))
        else:
            print_table(("FORMAT", "ECOSYSTEM", "THIRD-PARTY", "STANDARD", "RUNNABLE", "UNRESOLVED"),
                        [(item["format"], item["ecosystem"], item["verified_third_party"],
                          item["verified_standard"], item["runnable"],
                          item["unresolved_leads"]) for item in items])
        return 0
    if args.command == "catalog":
        catalog(args.format, args.ecosystem, args.json)
        return 0
    if args.command == "projects":
        projects(args.format, args.ecosystem, args.json)
        return 0
    if args.command == "show":
        show(args.format, args.ecosystem, args.slug, args.json)
        return 0
    if args.command == "build":
        project = ROOT / "projects" / args.format / args.ecosystem / args.slug
        if (project / "manifest.json").is_file() and json_file(project / "manifest.json").get(
                "coverage_kind") == "native_source_afl_feedback":
            return subprocess.call([sys.executable, str(project / "verify-control.py")], cwd=ROOT)
        return execute("run_project.py", args.format, args.ecosystem, args.slug)
    if args.command == "run":
        extra = ["--timeout", str(args.timeout)]
        if args.results:
            extra += ["--results", str(args.results)]
        return execute("run_case.py", args.format, args.ecosystem, args.slug,
                       str(args.file), *extra)
    if args.command == "replay":
        extra = ["--generator", args.generator, "--workers", str(args.workers),
                 "--timeout", str(args.timeout), "--batch-timeout", str(args.batch_timeout)]
        for name in ("generator_version", "spec", "spec_sha256", "generator_command"):
            if getattr(args, name):
                extra += ["--" + name.replace("_", "-"), getattr(args, name)]
        if args.per_case:
            extra.append("--per-case")
        return execute("replay_corpus.py", args.format, args.ecosystem, args.slug,
                       str(args.corpus), str(args.run_dir), *extra)
    if args.command == "run-format":
        extra = ["--workers", str(args.workers), "--timeout", str(args.timeout)]
        if args.ecosystem:
            extra += ["--ecosystem", args.ecosystem]
        if args.file:
            extra += ["--file", str(args.file)]
        if args.results:
            extra += ["--results", str(args.results)]
        if args.limit:
            extra += ["--limit", str(args.limit)]
        if args.list:
            extra.append("--list")
        return execute("run_format.py", args.format, *extra)
    if args.command == "afl":
        if args.action == "build":
            return build_afl(args.format, args.ecosystem, args.slug)
        if args.action == "prepare":
            extra = seed_arguments(args)
            if args.timeout_ms is not None:
                extra += ["--timeout-ms", str(args.timeout_ms)]
            return execute("prepare_afl_run.py", args.format, args.ecosystem, args.slug,
                           str(args.run_dir), *extra)
        if args.action == "run":
            extra = ["--seconds", str(args.seconds)]
            if args.check:
                extra.append("--check")
            if args.resume:
                extra.append("--resume")
            return execute("run_prepared_afl.py", str(args.run_dir), *extra)
        return execute("summarize_afl_run.py", str(args.run_dir))
    if args.command == "fandango":
        if args.action == "setup":
            return generator.setup()
        return generator.generate(fandango_generate, args)
    if args.action == "prepare":
        return execute("prepare_native_run.py", args.format, args.ecosystem, args.slug,
                       str(args.run_dir), *seed_arguments(args),
                       "--duration-seconds", str(args.duration_seconds))
    return execute("run_prepared_native.py", str(args.run_dir),
                   *(("--check",) if args.check else ()))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, StopIteration, KeyError) as error:
        raise SystemExit(f"parsarium: {error}") from error
