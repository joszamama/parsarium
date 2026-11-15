"""Preserve and replay a generated corpus through one Parsarium project.

Example: python3 scripts/replay_corpus.py png c libpng generated/png runs/png-libpng
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from run_case import MAX_CASE_BYTES, ROOT, project_for, run_case
from run_corpus_batch import run_batch


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("ecosystem")
    cli.add_argument("package_slug")
    cli.add_argument("corpus", type=Path)
    cli.add_argument("run_dir", type=Path)
    cli.add_argument("--workers", type=int, default=4)
    cli.add_argument("--timeout", type=int, default=60)
    cli.add_argument("--batch-timeout", type=int, default=3600)
    cli.add_argument("--per-case", action="store_true", help="skip the faster one-container replay")
    cli.add_argument("--generator", default="external")
    cli.add_argument("--generator-version")
    cli.add_argument("--spec", help="Fanbase name or local specification path")
    cli.add_argument("--spec-sha256", help="hash of an archived local specification")
    cli.add_argument("--generator-command", help="exact command used to generate the corpus")
    args = cli.parse_args()
    if args.workers < 1 or args.timeout < 1 or args.batch_timeout < 1:
        cli.error("workers and timeouts must be positive")
    project, manifest = project_for(args.format, args.ecosystem, args.package_slug)
    corpus = args.corpus.resolve(strict=True)
    if not corpus.is_dir():
        cli.error("corpus must be a directory")
    paths = sorted(path for path in corpus.rglob("*") if path.is_file())
    if not paths:
        cli.error("corpus is empty")
    run_dir = args.run_dir.resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        cli.error("run directory already contains files")
    if run_dir == corpus or run_dir.is_relative_to(corpus):
        cli.error("run directory must be outside the source corpus")
    cases = {}
    originals = []
    for path in paths:
        data = path.read_bytes()
        if len(data) > MAX_CASE_BYTES:
            cli.error(f"input exceeds {MAX_CASE_BYTES} bytes: {path}")
        digest = sha256(data).hexdigest()
        originals.append({"path": str(path.relative_to(corpus)), "sha256": digest,
                          "bytes": len(data)})
        cases.setdefault(digest, (path, data))
    inputs_dir = run_dir / "inputs"
    receipts_dir = run_dir / "executions"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir()
    for digest, (_, data) in cases.items():
        (inputs_dir / digest).write_bytes(data)
    def replay(digest: str) -> dict:
        outcome = run_case(project, manifest, inputs_dir / digest, args.timeout)
        return {"sha256": digest, **outcome}
    batch = None if args.per_case else run_batch(project, manifest, inputs_dir, args.batch_timeout)
    if batch is not None:
        (run_dir / "batch.json").write_text(json.dumps(batch, indent=2) + "\n")
        print(f"batch: {batch['status']} ({batch['input_count']} inputs)", flush=True)
    if batch is not None and batch["status"] == "ok":
        results = [{"sha256": digest, "status": "ok", "image_id": batch["image_id"],
                    "batch_replay": True} for digest in sorted(cases)]
        mode = "batch"
    else:
        results = []
        mode = "per_case" if batch is None else "batch_then_isolate"
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            pending = {pool.submit(replay, digest): digest for digest in sorted(cases)}
            for future in as_completed(pending):
                result = future.result()
                results.append(result)
                print(f"{result['sha256'][:12]} {result['status']}", flush=True)
    for result in results:
        (receipts_dir / f"{result['sha256']}.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n")
    results.sort(key=lambda item: item["sha256"])
    counts = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    summary = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(project.relative_to(ROOT / "projects")),
        "source_sha256": manifest["source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "image_ids": sorted({result["image_id"] for result in results if result.get("image_id")}),
        "generator": args.generator,
        "generator_version": args.generator_version,
        "spec": args.spec,
        "spec_sha256": args.spec_sha256,
        "generator_command": args.generator_command,
        "original_inputs": originals,
        "unique_inputs": len(cases),
        "execution_mode": mode,
        "batch_status": batch["status"] if batch is not None else None,
        "counts": counts,
        "input_limit_bytes": MAX_CASE_BYTES,
        "timeout_seconds": args.timeout,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"{len(cases)} unique inputs, {counts}")
    if counts.get("infrastructure_error") or counts.get("input_too_large"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
