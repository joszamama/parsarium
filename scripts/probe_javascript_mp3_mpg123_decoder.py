"""Reproduce the mpg123-decoder lead check on two valid untagged MP3 files.

The existing @audio/decode-mp3 Docker project pins mpg123-decoder 1.0.3 as a
transitive dependency. This probe calls mpg123-decoder directly; it neither
selects a plain-MP3 project nor starts a fuzz campaign.
"""

from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

from run_case import ROOT


IMAGE = "parsarium-candidate/mpg123-decoder:local"
PROJECT = ROOT / "projects/mp3/javascript/audio_decode_mp3"
REPORT = ROOT / "data/javascript/mp3/mpg123_decoder-feedback-blocked.json"
PACKAGE_SHA256 = "5207b35109ec884e7d47ab89b670bc86438399f681e1a6c26716003b3949cc5c"
PACKAGE_INTEGRITY = "sha512-+fjxnWigodWJm3+4pndi+KUg9TBojgn31DPk85zEsim7C6s0X5Ztc/hQYdytXkwuGXH+aB0/aEkG40Emukv6oQ=="
WASM_SHA256 = "f0e9e8848367320ccb757e4092f0d6809668cfe38f43139d47b447151d7dff6b"

CODE = r'''
import fs from "node:fs";
import crypto from "node:crypto";
import { MPEGDecoder } from "/work/node_modules/mpg123-decoder/index.js";
let wasmInfo = null;
const compile = WebAssembly.compile;
WebAssembly.compile = async function (bytes) {
  const buffer = Buffer.from(bytes);
  if (buffer.length > 50000) {
    const module = new WebAssembly.Module(buffer);
    wasmInfo = {
      bytes: buffer.length,
      sha256: crypto.createHash("sha256").update(buffer).digest("hex"),
      custom_sections: Object.fromEntries(
        ["name", ".debug_info", ".debug_line", "sourceMappingURL"].map(
          name => [name, WebAssembly.Module.customSections(module, name).length]
        )
      ),
      exports: WebAssembly.Module.exports(module).map(item => item.name),
    };
  }
  return compile.call(WebAssembly, bytes);
};
const decoder = new MPEGDecoder({ enableGapless: false });
await decoder.ready;
const result = decoder.decode(new Uint8Array(fs.readFileSync("/input/case")));
console.log(JSON.stringify({
  sample_rate: result.sampleRate,
  samples_decoded: result.samplesDecoded,
  channel_lengths: result.channelData.map(channel => channel.length),
  errors: result.errors,
  wasm: wasmInfo,
}));
decoder.free();
'''


def command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=1200)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args[:8])}: {(result.stdout + result.stderr)[-2500:]}")
    return result.stdout.strip()


def run_control(image: str, case: Path, coverage: Path | None) -> dict:
    args = ["docker", "run", "--rm", "--platform", "linux/arm64",
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,nosuid,size=64m",
            "-v", f"{case}:/input/case:ro"]
    if coverage is not None:
        args.extend(["-e", "NODE_V8_COVERAGE=/coverage", "-v", f"{coverage}:/coverage"])
    return json.loads(command([*args, "--entrypoint", "node", image,
                               "--input-type=module", "-e", CODE]))


def main() -> None:
    package_lock = json.loads((PROJECT / "package-lock.json").read_text())
    locked = package_lock["packages"]["node_modules/mpg123-decoder"]
    assert locked["version"] == "1.0.3" and locked["integrity"] == PACKAGE_INTEGRITY
    assert package_lock["packages"]["node_modules/@wasm-audio-decoders/common"]["version"] == "9.0.7"
    with tempfile.TemporaryDirectory(prefix="parsarium-mpg123-source-") as source_directory:
        source_tarball = Path(source_directory) / "mpg123-decoder-1.0.3.tgz"
        command(["curl", "--fail", "--location", "--silent", "--show-error",
                 "https://registry.npmjs.org/mpg123-decoder/-/mpg123-decoder-1.0.3.tgz",
                 "--output", str(source_tarball)])
        assert sha256(source_tarball.read_bytes()).hexdigest() == PACKAGE_SHA256
        with tarfile.open(source_tarball, "r:gz") as package:
            metadata = json.load(package.extractfile("package/package.json"))
            assert metadata["name"] == "mpg123-decoder" and metadata["version"] == "1.0.3"
            assert metadata["license"] == "MIT"
            assert not any(path.endswith("/LICENSE") for path in package.getnames())
    spec = importlib.util.spec_from_file_location("mp3_controls", ROOT / "controls/mp3/check_controls.py")
    oracle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(oracle)
    image = ""
    try:
        command(["docker", "build", "--quiet", "--platform", "linux/arm64",
                 "-t", IMAGE, str(PROJECT)])
        image = command(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"])
        controls = []
        with tempfile.TemporaryDirectory(prefix="parsarium-mpg123-decoder-") as temporary:
            for index, (filename, digest) in enumerate(oracle.CONTROLS.items()):
                case = oracle.ROOT / filename
                data = case.read_bytes()
                assert sha256(data).hexdigest() == digest
                walked = oracle.walk(data)
                coverage = Path(temporary) if index == 0 else None
                result = run_control(image, case, coverage)
                samples = walked["frames"] * walked["samples_per_frame"]
                assert result["sample_rate"] == walked["sample_rate"]
                assert result["samples_decoded"] == samples
                assert result["channel_lengths"] == [samples, samples]
                assert result["errors"] == []
                assert result["wasm"]["sha256"] == WASM_SHA256
                controls.append({"control": f"controls/mp3/{filename}", "sha256": digest,
                                 "oracle": walked, "verified_output": result})
            profiles = list(Path(temporary).glob("coverage-*.json"))
            assert len(profiles) == 1
            urls = [item["url"] for item in json.loads(profiles[0].read_text())["result"]]
            package_js = sorted({url.rsplit("/node_modules/", 1)[-1] for url in urls
                                 if "/node_modules/mpg123-decoder/" in url})
            wasm_scripts = [url for url in urls if url.startswith("wasm:")]
        wasm = controls[0]["verified_output"]["wasm"]
        assert wasm == controls[1]["verified_output"]["wasm"]
        assert wasm["bytes"] == 99479
        assert all(count == 0 for count in wasm["custom_sections"].values())
        assert not wasm_scripts
        result = {
            "schema_version": 1,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "candidate": "mpg123-decoder",
            "release": "1.0.3",
            "npm_downloads_30d": 2505430,
            "license_package": "MIT (package.json; no license file in npm tarball)",
            "underlying_family": "libmpg123; related to selected C mpg123 path, different pinned build",
            "underlying_license": "LGPL-2.1-only (libmpg123)",
            "source_repository_commit": "8f2428c1cd96b54dab74836c8471ff75fe35cbee",
            "mpg123_submodule_commit": "08247b317163175e62035893af3ff9e71a5dfefd",
            "source_tarball_sha256": PACKAGE_SHA256,
            "npm_integrity": PACKAGE_INTEGRITY,
            "dependency_fixture": "projects/mp3/javascript/audio_decode_mp3",
            "dependency_lock_sha256": sha256((PROJECT / "package-lock.json").read_bytes()).hexdigest(),
            "image_id": image,
            "documented_api": "new MPEGDecoder({enableGapless:false}); await ready; decode(Uint8Array(local bytes))",
            "documentation": "https://github.com/eshaz/wasm-audio-decoders/tree/8f2428c1cd96b54dab74836c8471ff75fe35cbee/src/mpg123-decoder",
            "controls": controls,
            "verified_scope": "sample rate and decoded samples per output channel on both valid untagged controls; decoder returns two PCM arrays for mono input, so channel count is not claimed",
            "wasm_module": wasm,
            "node_v8_profile_package_scripts": package_js,
            "node_v8_profile_wasm_scripts": wasm_scripts,
            "parser_source_line_coverage": None,
            "afl_parser_feedback": "blocked",
            "blocker": "The npm release embeds a compressed libmpg123 WASM module. The extracted pinned binary has no name, DWARF debug_info/debug_line, or sourceMappingURL custom sections; Node V8 coverage reports only JavaScript package wrappers and no WASM source scripts. Wrapper ranges cannot stand in for libmpg123 parser coverage. Source-attributed instrumentation would require rebuilding this package's C/WASM decoder with a pinned Emscripten toolchain and debug/coverage mapping, yielding a different binary whose equivalence to the shipped artifact is unverified.",
            "selection": "verified_control_feedback_blocked_unselected",
            "experiments": "two existing valid controls only; no malformed inputs or fuzz campaign",
        }
        REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(f"mpg123-decoder: valid controls pass; WASM source coverage and AFL feedback blocked")
    finally:
        if image:
            subprocess.run(["docker", "image", "rm", IMAGE], cwd=ROOT,
                           capture_output=True, text=True, check=False)


if __name__ == "__main__":
    main()
