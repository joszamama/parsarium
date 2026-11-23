"""Summarize AFL++'s saved feedback, queue, crashes, and hangs for one run."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


def inventory(directory: Path) -> list[dict]:
    if not directory.is_dir():
        return []
    files = []
    for path in sorted(directory.iterdir()):
        if not path.is_file() or path.name.startswith("README"):
            continue
        data = path.read_bytes()
        files.append({"name": path.name, "sha256": sha256(data).hexdigest(),
                      "bytes": len(data)})
    return files


def stats(path: Path) -> dict:
    result = {}
    if path.is_file():
        for line in path.read_text().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()
    return result


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("run_dir", type=Path)
    args = cli.parse_args()
    run_dir = args.run_dir.resolve(strict=True)
    plan = json.loads((run_dir / "plan.json").read_text())
    output = run_dir / "afl-out"
    instances = sorted(path for path in output.iterdir() if (path / "fuzzer_stats").is_file())
    if not instances:
        cli.error("no AFL++ fuzzer_stats found; the prepared campaign has not run")
    report = {"schema_version": 1, "project": plan["project"],
              "image_id": plan["image_id"], "unique_seeds": plan["unique_seeds"],
              "seed_generation": plan.get("seed_generation"), "instances": []}
    for instance in instances:
        queue = inventory(instance / "queue")
        report["instances"].append({
            "name": instance.name,
            "fuzzer_stats": stats(instance / "fuzzer_stats"),
            # AFL++ names imported seeds "id:N,time:0,execs:0,orig:NAME".
            "initial_queue_entries": sum(1 for item in queue if ",orig:" in item["name"]),
            "queue": queue,
            "crashes": inventory(instance / "crashes"),
            "hangs": inventory(instance / "hangs"),
        })
    (run_dir / "afl-summary.json").write_text(json.dumps(report, indent=2) + "\n")
    for instance in report["instances"]:
        values = instance["fuzzer_stats"]
        print(f"{instance['name']}: execs={values.get('execs_done', '?')} "
              f"seeds={instance['initial_queue_entries']} "
              f"paths={len(instance['queue'])} crashes={len(instance['crashes'])} "
              f"hangs={len(instance['hangs'])}")


if __name__ == "__main__":
    main()
