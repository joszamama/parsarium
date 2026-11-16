"""Stage one locked Rust crate with a source-instrumented replay and libFuzzer entry.

Currently supports cell adapters with a `parse(package, path)` function. Staging
alone is not verification: build the container and run the AFL++ and smoke checks.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
FORMATS = {"ascii_ply", "ascii_pnm", "http11", "svg", "mp3_id3v2", "mp4", "pdf", "wav", "png", "zip"}
MAIN_ADAPTERS = {"ascii_ply", "ascii_pnm", "http11", "svg"}
OUTPUT_ADAPTERS = {"png", "zip"}


def stage(format_name: str, package: str) -> Path:
    if format_name not in FORMATS:
        raise ValueError(f"Rust adapter structure is not supported: {format_name}")
    catalog = ROOT / "data/rust" / format_name / "parsers.json"
    parser, = [item for item in json.loads(catalog.read_text()) if item["name"] == package]
    for old in (ROOT / "projects" / format_name / "rust").glob("*/manifest.json"):
        if json.loads(old.read_text()).get("package") == package:
            raise ValueError(f"already staged: {old.parent}")
    cell = ROOT / "adapters/rust" / format_name
    original = (cell / "src/main.rs").read_text()
    parse_end = original.index("fn main(")
    source = original if format_name in MAIN_ADAPTERS | OUTPUT_ADAPTERS else original[:parse_end]
    arm_re = re.compile(r'(?m)^        "([^"\n]+)" => \{')
    arms = list(arm_re.finditer(source))
    selected, = [i for i, arm in enumerate(arms) if arm.group(1) == package]
    default_match = re.search(r"(?m)^        (?:_|other) =>", source[arms[-1].end():])
    if default_match is None:
        raise ValueError("adapter has no default match arm")
    default = arms[-1].end() + default_match.start()
    arm_end = arms[selected + 1].start() if selected + 1 < len(arms) else default
    source = source[:arms[0].start()] + source[arms[selected].start():arm_end] + source[default:]
    if format_name in MAIN_ADAPTERS | OUTPUT_ADAPTERS:
        source = re.sub(r"fn main\(\) -> Result<\(\), Box<dyn (?:std::error::)?Error>> \{",
                        "fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {",
                        source, count=1)
        source = source.replace("env::args().collect()", "vec![\"parser\".into(), package.into(), path.to_string_lossy().into_owned()]", 1)
        if format_name in MAIN_ADAPTERS:
            source = source.replace('    println!("{output}");\n    Ok(())', '    Ok(output)', 1)
        elif format_name == "png":
            source, replaced = re.subn(r"println!\((.*?)\);",
                lambda match: "return Ok(serde_json::from_str(&format!(" + match.group(1) + "))?);",
                source, count=1, flags=re.S)
            if replaced != 1:
                raise ValueError("PNG adapter did not print one result")
            source = source.replace("    Ok(())\n}", '    Err("parser produced no result".into())\n}', 1)
        else:
            source = source.replace('fn output(name: &str, content: Option<&str>, size: u64) {\n    println!("{}", serde_json::json!({"name": name, "content": content, "size": size}));\n}',
                'fn output(name: &str, content: Option<&str>, size: u64) -> serde_json::Value {\n    serde_json::json!({"name": name, "content": content, "size": size})\n}')
            source = source.replace('fn output_entry(name: &str, count: usize) {\n    println!("{}", serde_json::json!({"name": name, "entry_count": count}));\n}',
                'fn output_entry(name: &str, count: usize) -> serde_json::Value {\n    serde_json::json!({"name": name, "entry_count": count})\n}')
            source = re.sub(r"(?m)^(\s*)(output(?:_entry)?)\((.*)\);$",
                            r"\1return Ok(\2(\3));", source)
            source = source.replace("    Ok(())\n}", '    Err("parser produced no result".into())\n}', 1)
            if format_name == "zip" and package in {"async_zip", "astral_async_zip"}:
                source = source.replace("pollster::block_on(async {", "return pollster::block_on(async {", 1)
                source = source.replace(
                    "return Ok(output(&name, Some(&content), size));\n"
                    "                Ok::<(), Box<dyn Error>>(())\n            })?;",
                    "Ok::<serde_json::Value, Box<dyn Error>>(output(&name, Some(&content), size))\n"
                    "            });", 1)
        if "fn parse_package(" not in source or '    println!("{output}");' in source:
            raise ValueError("could not transform cell main into parser function")
    else:
        source = source.replace("fn parse(", "fn parse_package(", 1)
    source += f'''
use std::sync::atomic::{{AtomicU64, Ordering}};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn std::error::Error>> {{
    if data.is_empty() || data.len() > (1 << 20) {{
        return Err("input outside harness limit".into());
    }}
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{{}}-{{}}{Path(parser['control']).suffix}",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package({json.dumps(package)}, &path);
    std::fs::remove_file(path)?;
    outcome
}}
'''
    cell_manifest = tomllib.loads((cell / "Cargo.toml").read_text())
    dependency_lines = {}
    for line in (cell / "Cargo.toml").read_text().splitlines():
        match = re.match(r"^([\w-]+)\s*=\s*", line)
        if match and match.group(1) in cell_manifest["dependencies"]:
            dependency_lines[match.group(1)] = line
    if format_name == "png":
        dependency_lines["serde_json"] = 'serde_json = "=1.0.145"'
    dependencies = cell_manifest["dependencies"]
    def cargo_name(key: str) -> str:
        value = dependencies[key]
        return value.get("package", key) if isinstance(value, dict) else key
    candidates = [key for key in dependencies if key == package or cargo_name(key) == package]
    if not candidates:
        raise ValueError(f"no cell dependency for {package}")
    target = package if package in candidates else candidates[0]
    referenced = set(re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)::", source))
    chosen = {target, "serde_json"}
    chosen.update(key for key in dependencies if key.replace("-", "_") in referenced)
    missing = chosen - dependency_lines.keys()
    if missing:
        raise ValueError(f"missing dependency declarations: {missing}")
    slug = re.sub(r"[^a-z0-9]+", "_", package.lower()).strip("_")
    destination = ROOT / "projects" / format_name / "rust" / slug
    if destination.exists():
        raise ValueError(f"path exists: {destination}")
    destination.mkdir(parents=True)
    lib_name = f"parsarium_{format_name}_{slug}_harness"
    package_name = lib_name.replace("_", "-")
    cargo = f'''[package]
name = "{package_name}"
version = "0.1.0"
edition = "2024"

[dependencies]
{chr(10).join(dependency_lines[key] for key in sorted(chosen))}
libfuzzer-sys = {{ version = "=0.4.13", optional = true }}

[features]
fuzzing = ["dep:libfuzzer-sys"]

[[bin]]
name = "replay"
path = "src/bin/replay.rs"

[[bin]]
name = "fuzzer"
path = "src/bin/fuzzer.rs"
required-features = ["fuzzing"]
'''
    (destination / "Cargo.toml").write_text(cargo)
    bins = destination / "src/bin"
    bins.mkdir(parents=True)
    (destination / "src/lib.rs").write_text(source)
    (bins / "replay.rs").write_text(f'''use {lib_name}::parse;
fn main() -> Result<(), Box<dyn std::error::Error>> {{
    let path = std::env::args().nth(1).ok_or("expected input path")?;
    println!("{{}}", parse(&std::fs::read(path)?)?);
    Ok(())
}}
''')
    (bins / "fuzzer.rs").write_text(f'''#![no_main]
use libfuzzer_sys::fuzz_target;
use {lib_name}::parse;
fuzz_target!(|data: &[u8]| {{ let _ = parse(data); }});
''')
    result = subprocess.run(["cargo", "generate-lockfile"], cwd=destination,
                            capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr[-1600:])
    lock = tomllib.loads((destination / "Cargo.lock").read_text())
    crate_name = cargo_name(target)
    crate, = [entry for entry in lock["package"]
              if entry["name"] == crate_name and entry["version"] == parser["version"]]
    digest = crate["checksum"]
    crate_dir = f"{crate_name}-{parser['version']}"
    coverage_crate = (f"threecrate-io-{parser['version']}"
                      if format_name == "ascii_ply" and package == "threecrate"
                      else "zip-1.3.1" if format_name == "zip" and package == "zip_next"
                      else f"zpdf-parser-{parser['version']}" if format_name == "pdf" and package == "zpdf"
                      else crate_dir)
    template = ROOT / "projects/mp4/rust/mp4"
    docker = (template / "Dockerfile").read_text()
    docker = docker.replace("mp4-0.14.0", crate_dir).replace(
        "c9ef834d5ed55e494a2ae350220314dc4aacd1c43a9498b00e320e0ea352a5c3", digest)
    docker = docker.replace("mp4-source", "parser-source")
    (destination / "Dockerfile").write_text(docker)
    expected = json.dumps(parser["expected_output"], separators=(",", ":"))
    control_script = (template / "run-control.sh").read_text()
    control_script = re.sub(r"expected = \{.*?\}",
                            lambda _: f"expected = json.loads({repr(expected)})", control_script)
    control_script = control_script.replace("/mp4-0.14.0/", f"/{coverage_crate}/")
    control_script = control_script.replace("mp4 crate", f"{coverage_crate} crate")
    (destination / "run-control.sh").write_text(control_script)
    (destination / "source-lock.json").write_text(json.dumps({package: {
        "release": parser["version"], "source_sha256": digest}}, indent=2) + "\n")
    control = ROOT / parser["control"]
    manifest = json.loads((template / "manifest.json").read_text())
    manifest.pop("format_specific_coverage_file_suffix", None)
    manifest.update({"format": format_name, "package": package,
                     "release": parser["version"],
                     "catalog_parser": str(catalog.relative_to(ROOT)),
                     "source_lock": str((destination / "source-lock.json").relative_to(ROOT)),
                     "source_sha256": digest, "control": parser["control"],
                     "control_sha256": sha256(control.read_bytes()).hexdigest(),
                     "expected_output": parser["expected_output"],
                     "coverage": f"Rust LLVM source coverage in {coverage_crate}; libFuzzer sanitizer counters",
                     "coverage_subject_prefix": "/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/" + coverage_crate + "/"})
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("package")
    args = cli.parse_args()
    print(stage(args.format, args.package).relative_to(ROOT))
