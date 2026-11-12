"""Run pinned Go ASCII PLY adapters against the valid local triangle control."""

import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "ascii_ply"
MODULE = ROOT / "adapters" / "go" / "ascii_ply"
CONTROL = ROOT / "controls" / "ascii_ply" / "triangle.ply"
NATIVE = {
    "github.com/NOT-REAL-GAMES/assimpgo": "native_notreal",
    "github.com/tbogdala/assimp-go": "native_tbogdala",
    "github.com/sg3des/assimp-go": "native_sg3des",
    "github.com/PetrusJPrinsloo/assimp-go": "native_petrus",
}


def output_of(*command: str) -> str:
    return subprocess.check_output(command, cwd=MODULE, text=True).strip()


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    native_dir = output_of("bash", str(ROOT / "scripts" / "prepare_go_ascii_ply_native.sh"))
    assimp_flags = output_of("pkg-config", "--cflags", "assimp")
    assimp_libs = output_of("pkg-config", "--libs", "assimp")
    assimp_libdir = output_of("pkg-config", "--variable=libdir", "assimp")
    base_env = os.environ.copy()
    base_env.pop("CGO_CFLAGS", None)
    base_env["CGO_LDFLAGS"] = f"-L{native_dir} {assimp_libs}"
    base_env["DYLD_LIBRARY_PATH"] = ":".join(filter(None, [native_dir, assimp_libdir, base_env.get("DYLD_LIBRARY_PATH")]))
    results = []
    for parser in parsers:
        name = parser["name"]
        if name in NATIVE:
            command = ["go", "run", f"./{NATIVE[name]}", "../../../controls/ascii_ply/triangle.ply"]
        else:
            command = ["go", "run", ".", name, "../../../controls/ascii_ply/triangle.ply"]
        env = base_env.copy()
        if name in NATIVE:
            env["CGO_CFLAGS"] = assimp_flags
        output = None
        error = None
        try:
            run = subprocess.run(command, cwd=MODULE, env=env, text=True, capture_output=True, timeout=180, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({
            "package": name, "module": parser["module"], "version": parser["version"],
            "scope": parser["scope"], "command": " ".join(command),
            "pass": passed, "output": output, "error": error,
            "native_environment": "assimp cflags and libs from pkg-config; local Greg Turk plyfile archive and bundled Assimp 5 runtime" if name in NATIVE else "assimp libs from pkg-config; local Greg Turk plyfile archive and bundled Assimp 5 runtime",
        })
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "go": output_of("go", "version"),
        "assimp": output_of("pkg-config", "--modversion", "assimp"),
        "control": "controls/ascii_ply/triangle.ply",
        "control_sha256": hashlib.sha256(CONTROL.read_bytes()).hexdigest(),
        "control_meaning": "Valid ASCII PLY with three vertices and one triangle face",
        "native_setup": "bash scripts/prepare_go_ascii_ply_native.sh",
        "third_party": results,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in results)
    print(f"{passed}/{len(results)} Go ASCII PLY packages passed")
    if passed != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
