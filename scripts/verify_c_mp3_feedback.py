"""Check the C plain MP3 AFL++ overlays: repeated control maps match and a second valid control differs.

For each requested path (default: all), the base project image replays the
differential control against its pinned expected output. The AFL++ overlay then
maps each valid control REPEATS times with afl-showmap; tuples must repeat
exactly per control and differ between them. Records of paths not requested are
kept from the existing report with their own check time.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for


SCOPES = {
    "mpg123": ("afl_clang_fast_libmpg123_and_harness_edges",
               "AFL++ instruments only the pinned libmpg123 sources and the feed-API harness; no other library is compiled into /work/fuzzer."),
    "libmad": ("afl_clang_fast_libmad_and_harness_edges",
               "AFL++ instruments only the pinned libmad sources and the mad_stream_buffer/mad_frame_decode/mad_synth_frame harness; no other library is compiled into /work/fuzzer."),
}
REPEATS = 5
REPORT = ROOT / "data/c/mp3/afl-feedback.json"


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(platform: str, mounts: list[str]) -> list[str]:
    return ["docker", "run", "--rm", "--platform", platform,
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp", *mounts]


def showmap(manifest: dict, receipt: dict, case: Path, work: Path, name: str) -> set[str]:
    run([*sandbox(manifest["platform"], ["-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]),
         "-e", f"AFL_MAP_SIZE={receipt['afl_map_size']}", "--entrypoint", "afl-showmap",
         receipt["image_id"], "-m", "none", "-t", "10000", "-o", f"/coverage/{name}.map",
         "--", "/work/fuzzer", "/input/case"])
    return set((work / f"{name}.map").read_text().splitlines()) - {""}


def check(slug: str) -> dict:
    project, manifest = project_for("mp3", "c", slug)
    relative = Path("mp3/c") / slug
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise ValueError("overlay receipt does not match the base project receipt")
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    digests = [manifest["control_sha256"], manifest["differential_control_sha256"]]
    for path, digest in zip(controls, digests):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")

    replay = run([*sandbox(manifest["platform"], ["-v", f"{controls[1]}:/input/differential:ro"]),
                  "--entrypoint", "/work/replay", base["image_id"], "/input/differential"])
    observed = json.loads(replay)
    if observed != manifest["differential_expected_output"]:
        raise RuntimeError(f"differential control output mismatch: {observed}")

    maps: list[set[str]] = []
    with tempfile.TemporaryDirectory(prefix=f"parsarium-mp3-c-{slug}-") as temporary:
        work = Path(temporary)
        for index, control in enumerate(controls):
            runs = [showmap(manifest, receipt, control, work, f"c{index}r{repeat}")
                    for repeat in range(REPEATS)]
            if any(item != runs[0] for item in runs):
                raise RuntimeError(f"{control.name}: repeated AFL++ maps differ")
            maps.append(runs[0])
    if len(maps[0]) != receipt["feedback_edges"]:
        raise RuntimeError("control map differs from overlay receipt")
    tuple_difference = len({item.split(":", 1)[0] for item in maps[0]} ^
                           {item.split(":", 1)[0] for item in maps[1]})
    if not tuple_difference:
        raise RuntimeError("differential control did not change AFL++ feedback")
    print(f"{relative}: stable repeats; {len(maps[0])} vs {len(maps[1])} tuples, "
          f"{tuple_difference} edge ids differ", flush=True)
    kind, scope = SCOPES[slug]
    return {
        "project": str(relative),
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "pass": True,
        "feedback_kind": kind,
        "feedback_scope": scope,
        "base_project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"],
        "overlay_image_id": receipt["image_id"],
        "repeats_per_control": REPEATS,
        "repeated_controls_identical": True,
        "first_control": manifest["control"],
        "first_sha256": manifest["control_sha256"],
        "second_control": manifest["differential_control"],
        "second_sha256": manifest["differential_control_sha256"],
        "second_control_output": observed,
        "second_case_kind": "valid_control",
        "first_afl_tuples": len(maps[0]),
        "second_afl_tuples": len(maps[1]),
        "afl_tuple_difference": tuple_difference,
    }


def previous() -> dict[str, dict]:
    if not REPORT.exists():
        return {}
    report = json.loads(REPORT.read_text())
    if report.get("schema_version") == 1:
        record = {key: value for key, value in report.items() if key != "schema_version"}
        return {record["project"]: record}
    return {item["project"]: item for item in report["results"]}


def main() -> None:
    slugs = sys.argv[1:] or list(SCOPES)
    unknown = set(slugs) - set(SCOPES)
    if unknown:
        raise SystemExit(f"unknown C MP3 paths: {sorted(unknown)}")
    records = previous()
    for slug in slugs:
        records[f"mp3/c/{slug}"] = check(slug)
    results = [records[f"mp3/c/{slug}"] for slug in SCOPES if f"mp3/c/{slug}" in records]
    REPORT.write_text(json.dumps({
        "schema_version": 2,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results),
        "projects_passed": sum(item["pass"] for item in results),
        "pass": all(item["pass"] for item in results),
        "results": results,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
