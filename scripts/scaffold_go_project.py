"""Stage one pinned Go parser with a format-specific byte harness and Go coverage."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "projects/png/go/imaging"
BASE_IMAGE = "golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66"


def stage(format_name: str, package: str) -> Path:
    cell = ROOT / "data/go" / format_name
    catalog = cell / "parsers.json"
    parser, = [item for item in json.loads(catalog.read_text()) if item["name"] == package]
    verification = json.loads((cell / "verification.json").read_text())
    record = next(item for item in verification["third_party"] if item["package"] == package)
    if not record["pass"]:
        raise ValueError("saved parser control did not pass")
    command = record.get("command", "")
    match = re.search(r"controls/[A-Za-z0-9_./-]+", command)
    control = match.group() if match else verification.get("control")
    if not control or not (ROOT / control).is_file():
        raise ValueError(f"no saved valid control for {package}")
    expected = parser.get("expected_output", record["output"])
    module = parser.get("module", package)
    version = parser["version"]
    adapter = ROOT / "adapters/go" / format_name
    source = adapter / "main.go"
    if not source.is_file():
        raise ValueError("no format-specific Go adapter")
    native = False
    if package not in source.read_text():
        native_sources = [item for item in adapter.glob("native_*/main.go")
                          if module.lower() in item.read_text().lower()
                          or package.lower() in item.read_text().lower()]
        if len(native_sources) != 1:
            raise ValueError(f"cannot locate one native adapter for {package}")
        source = native_sources[0]
        native = True
    result = subprocess.run(["go", "mod", "download", "-json", f"{module}@{version}"],
                            cwd=adapter, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError(result.stderr[-1000:])
    downloaded = json.loads(result.stdout)
    zip_path = Path(downloaded["Zip"])
    digest = sha256(zip_path.read_bytes()).hexdigest()
    go_sum = downloaded["Sum"]
    escaped_module = "".join("!" + letter.lower() if letter.isupper() else letter for letter in module)
    slug = re.sub(r"[^a-z0-9]+", "_", package.lower()).strip("_")
    destination = ROOT / "projects" / format_name / "go" / slug
    if destination.exists():
        raise ValueError(f"project exists: {destination}")
    destination.mkdir(parents=True)
    shutil.copyfile(adapter / "go.mod", destination / "go.mod")
    shutil.copyfile(adapter / "go.sum", destination / "go.sum")
    slice_tool = ROOT / "scripts/slice_go_adapter.go"
    if native:
        shutil.copyfile(source, destination / "adapter.go")
    else:
        cut = subprocess.run(["go", "run", str(slice_tool), "--", str(source), package,
                              str(destination / "adapter.go")], cwd=ROOT,
                             capture_output=True, text=True, timeout=60)
        if cut.returncode:
            raise RuntimeError(cut.stderr[-1000:])
    has_run = bool(re.search(r"func run\(", source.read_text()))
    if has_run:
        if re.search(r"func run\(name string, data \[\]byte\)", source.read_text()):
            parse_helper = ("func parseControl(source string) (map[string]any, error) { "
                            "data, err := os.ReadFile(source); if err != nil { return nil, err }; "
                            "return run(parserName, data) }")
        else:
            parse_helper = "func parseControl(source string) (map[string]any, error) { return run(parserName, source) }"
        extra_import = ""
    else:
        extra_import = '    "bytes"\n    "io"\n'
        argv = '[]string{"parser", source}' if native else '[]string{"parser", parserName, source}'
        parse_helper = '''func parseControl(source string) (map[string]any, error) {
    reader, writer, err := os.Pipe()
    if err != nil { return nil, err }
    originalStdout, originalArgs := os.Stdout, os.Args
    os.Stdout, os.Args = writer, ''' + argv + '''
    defer func() { os.Stdout, os.Args = originalStdout, originalArgs; reader.Close(); writer.Close() }()
    main()
    writer.Close()
    data, err := io.ReadAll(reader)
    if err != nil { return nil, err }
    data = bytes.TrimSpace(data)
    if split := bytes.LastIndexByte(data, '\\n'); split >= 0 { data = data[split+1:] }
    var output map[string]any
    err = json.Unmarshal(data, &output)
    return output, err
}'''
    expected_json = json.dumps(expected, separators=(",", ":"))
    test = f'''package main

import (
    "encoding/json"
    "fmt"
{extra_import}    "os"
    "path/filepath"
    "reflect"
    "testing"
)

const parserName = {json.dumps(package)}
const expectedJSON = {json.dumps(expected_json)}

{parse_helper}

func TestControl(t *testing.T) {{
    got, err := parseControl("/input/control")
    if err != nil {{ t.Fatal(err) }}
    encoded, err := json.Marshal(got)
    if err != nil {{ t.Fatal(err) }}
    var observed, expected any
    if err := json.Unmarshal(encoded, &observed); err != nil {{ t.Fatal(err) }}
    if err := json.Unmarshal([]byte(expectedJSON), &expected); err != nil {{ t.Fatal(err) }}
    if !reflect.DeepEqual(observed, expected) {{ t.Fatalf("control mismatch: %s", encoded) }}
    fmt.Printf("OBSERVED_JSON:%s\\n", encoded)
}}

func FuzzParser(f *testing.F) {{
    f.Fuzz(func(t *testing.T, data []byte) {{
        if len(data) == 0 || len(data) > (1 << 20) {{ return }}
        directory := t.TempDir()
        source := filepath.Join(directory, "input{Path(control).suffix}")
        if err := os.WriteFile(source, data, 0600); err != nil {{ t.Fatal(err) }}
        _, _ = parseControl(source)
    }})
}}
'''
    (destination / "harness_test.go").write_text(test)
    reporter = (TEMPLATE / "reporter/main.go").read_text()
    reporter = reporter.replace('const packagePrefix = "github.com/disintegration/imaging/"',
                                f'const packagePrefix = {json.dumps(package + "/")}')
    reporter = reporter.replace('const underlyingPrefix = "image/png/"',
                                'const underlyingPrefix = "\\x00"')
    reporter = reporter.replace('if packageFiles == 0 || underlyingFiles == 0 || total == 0 || underlyingLines == 0 {',
                                'if packageFiles == 0 || total == 0 {')
    (destination / "reporter").mkdir()
    (destination / "reporter/main.go").write_text(reporter)
    cgo = "1" if native else "0"
    toolchain = "ENV GOTOOLCHAIN=auto\n" if format_name == "pdf" else ""
    docker = f'''FROM --platform=linux/arm64 {BASE_IMAGE} AS build
{toolchain}WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \\
    && echo '{digest}  /go/pkg/mod/cache/download/{escaped_module}/@v/{version}.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED={cgo} go test -c -coverpkg={package} -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
'''
    (destination / "Dockerfile").write_text(docker)
    (destination / "source-lock.json").write_text(json.dumps({package: {
        "release": version, "source_sha256": digest, "go_module_sum": go_sum,
        "go_module": module}}, indent=2) + "\n")
    manifest = json.loads((TEMPLATE / "manifest.json").read_text())
    for key in ("underlying_coverage_subject_prefix", "format_specific_coverage_file_suffix"):
        manifest.pop(key, None)
    manifest.update({"format": format_name, "package": package, "release": version,
                     "catalog_parser": str(catalog.relative_to(ROOT)),
                     "source_lock": str((destination / "source-lock.json").relative_to(ROOT)),
                     "source_sha256": digest, "control": control,
                     "control_sha256": sha256((ROOT / control).read_bytes()).hexdigest(),
                     "expected_output": expected, "harness": "harness_test.go", "fuzz_entry": "FuzzParser",
                     "fuzz_smoke_expect": "FuzzParser", "coverage_subject_prefix": package + "/",
                     "coverage": f"Go test coverpkg instrumentation of {package} during valid-control replay"})
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("package")
    args = cli.parse_args()
    print(stage(args.format, args.package).relative_to(ROOT))
