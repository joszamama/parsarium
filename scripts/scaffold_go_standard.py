"""Stage the six documented Go standard-library parser paths as separate targets."""

from hashlib import sha256
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = "golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66"
GO_SHA = "1675694ef690db0f18fbe7046a886170904bede1d9db6ec96ae27945c1705c64"
RUNTIME = "Go 1.27.1 linux/arm64 standard library"
SOURCE = {
    "request": ("net/http", "net/http/request.go", "c3257079994b4e4f74f01cef72508919983ba31f91fcf599d348e9d52cec1540"),
    "response": ("net/http", "net/http/response.go", "0b32a0b4ee51e00e3410764f3b2ffe1163dccb9cad548b097f47db85893a2f44"),
    "decode": ("image/png", "image/png/reader.go", "f6e97084ce561f92ae7658b34f16d797aa46c65325b2ae9cd931d0f2434993c1"),
    "config": ("image/png", "image/png/reader.go", "f6e97084ce561f92ae7658b34f16d797aa46c65325b2ae9cd931d0f2434993c1"),
    "generic": ("image", "image/format.go", "53132521ce77410e84a241c3a0948949b7e164ff4503ea618adec4c1ddffdc66"),
    "openreader": ("archive/zip", "archive/zip/reader.go", "d35e8e55c85c222c16b29f8976a51698533c3874ff478427794a29af7b23e417"),
}
EXPECTED = {
    "request": {"host": "example.test", "method": "GET", "proto": "HTTP/1.1", "target": "/parsarium?x=1"},
    "response": {"body": "parsarium", "proto": "HTTP/1.1", "status": 200},
    "decode": {"height": 1, "rgba": [255, 0, 0, 255, 0, 255, 0, 255], "width": 2},
    "config": {"height": 1, "width": 2},
    "generic": {"format": "png", "height": 1, "width": 2},
    "openreader": {"name": "hello.txt", "text": "parsarium\n"},
}
API_PREFIX = {
    "request": "net/http.ReadRequest", "response": "net/http.ReadResponse",
    "decode": "image/png.Decode(io.Reader)",
    "config": "image/png.DecodeConfig(io.Reader)",
    "generic": "image.Decode(io.Reader)",
    "openreader": "archive/zip.OpenReader",
}
FORMAT = {"request": "http11", "response": "http11", "decode": "png",
          "config": "png", "generic": "png", "openreader": "zip"}
ADAPTER = {
    "request": '''package main
import ("bufio";"bytes";"net/http")
func Parse(data []byte) (map[string]any,error) {
 r,e:=http.ReadRequest(bufio.NewReader(bytes.NewReader(data)));if e!=nil{return nil,e};defer r.Body.Close()
 return map[string]any{"host":r.Host,"method":r.Method,"proto":r.Proto,"target":r.URL.RequestURI()},nil
}
''',
    "response": '''package main
import ("bufio";"bytes";"io";"net/http")
func Parse(data []byte) (map[string]any,error) {
 r,e:=http.ReadResponse(bufio.NewReader(bytes.NewReader(data)),&http.Request{Method:"GET"});if e!=nil{return nil,e};defer r.Body.Close()
 b,e:=io.ReadAll(r.Body);if e!=nil{return nil,e}
 return map[string]any{"status":r.StatusCode,"proto":r.Proto,"body":string(b)},nil
}
''',
    "decode": '''package main
import ("bytes";"image/color";"image/png")
func Parse(data []byte) (map[string]any,error) {
 im,e:=png.Decode(bytes.NewReader(data));if e!=nil{return nil,e}
 a:=color.NRGBAModel.Convert(im.At(0,0)).(color.NRGBA);b:=color.NRGBAModel.Convert(im.At(1,0)).(color.NRGBA)
 return map[string]any{"width":im.Bounds().Dx(),"height":im.Bounds().Dy(),"rgba":[]int{int(a.R),int(a.G),int(a.B),int(a.A),int(b.R),int(b.G),int(b.B),int(b.A)}},nil
}
''',
    "config": '''package main
import ("bytes";"image/png")
func Parse(data []byte) (map[string]any,error) {
 cfg,e:=png.DecodeConfig(bytes.NewReader(data));if e!=nil{return nil,e}
 return map[string]any{"width":cfg.Width,"height":cfg.Height},nil
}
''',
    "generic": '''package main
import ("bytes";"image";_ "image/png")
func Parse(data []byte) (map[string]any,error) {
 im,format,e:=image.Decode(bytes.NewReader(data));if e!=nil{return nil,e}
 return map[string]any{"format":format,"width":im.Bounds().Dx(),"height":im.Bounds().Dy()},nil
}
''',
    "openreader": '''package main
import ("archive/zip";"io";"os")
func Parse(data []byte) (map[string]any,error) {
 f,e:=os.CreateTemp("","parsarium-zip-*.zip");if e!=nil{return nil,e};defer os.Remove(f.Name())
 if _,e=f.Write(data);e!=nil{f.Close();return nil,e};if e=f.Close();e!=nil{return nil,e}
 z,e:=zip.OpenReader(f.Name());if e!=nil{return nil,e};defer z.Close()
 if len(z.File)!=1{return nil,io.ErrUnexpectedEOF};r,e:=z.File[0].Open();if e!=nil{return nil,e};defer r.Close()
 b,e:=io.ReadAll(r);if e!=nil{return nil,e}
 return map[string]any{"name":z.File[0].Name,"text":string(b)},nil
}
''',
}


def stage(name: str) -> Path:
    fmt = FORMAT[name]
    inventory_path = ROOT / "data/go" / fmt / "standard.json"
    inventory = json.loads(inventory_path.read_text())
    entry, = [item for item in inventory["verified_apis"]
              if item["api"].startswith(API_PREFIX[name])]
    entry["runtime"] = RUNTIME
    entry["expected"] = EXPECTED[name]
    inventory_path.write_text(json.dumps(inventory, indent=2) + "\n")
    destination = ROOT / "projects" / fmt / "go" / ("stdlib_" + name)
    if destination.exists():
        raise ValueError(destination)
    destination.mkdir(parents=True)
    subject, source_path, digest = SOURCE[name]
    (destination / "go.mod").write_text("module parsarium/stdlib-harness\n\ngo 1.27.1\n")
    (destination / "adapter.go").write_text(ADAPTER[name])
    (destination / "harness_test.go").write_text('''package main
import ("encoding/json";"fmt";"os";"reflect";"testing")
const expectedJSON = EXPECTED_JSON
func TestControl(t *testing.T) {
 data,e:=os.ReadFile("/input/control");if e!=nil{t.Fatal(e)}
 got,e:=Parse(data);if e!=nil{t.Fatal(e)}
 var want map[string]any;if e=json.Unmarshal([]byte(expectedJSON),&want);e!=nil{t.Fatal(e)}
 var normalized map[string]any;b,_:=json.Marshal(got);if e=json.Unmarshal(b,&normalized);e!=nil{t.Fatal(e)}
 if !reflect.DeepEqual(normalized,want){t.Fatalf("control mismatch: %s",b)}
 fmt.Printf("OBSERVED_JSON:%s\\n",b)
}
func FuzzParser(f *testing.F){f.Fuzz(func(t *testing.T,data []byte){if len(data)>0&&len(data)<(1<<20){_,_=Parse(data)}})}
'''.replace("EXPECTED_JSON", json.dumps(json.dumps(EXPECTED[name]))))
    reporter = (ROOT / "projects/png/go/imaging/reporter/main.go").read_text()
    reporter = reporter.replace('const packagePrefix = "github.com/disintegration/imaging/"',
                                f'const packagePrefix = "{subject}/"')
    underlying = "image/png/" if name == "generic" else "__none__/"
    reporter = reporter.replace('const underlyingPrefix = "image/png/"',
                                f'const underlyingPrefix = "{underlying}"')
    if name != "generic":
        reporter = reporter.replace(
            'if packageFiles == 0 || underlyingFiles == 0 || total == 0 || underlyingLines == 0 {',
            'if packageFiles == 0 || total == 0 {')
    else:
        reporter = reporter.replace(
            '} else if strings.HasPrefix(name, underlyingPrefix) {',
            '}\n        if strings.HasPrefix(name, underlyingPrefix) {')
    (destination / "reporter").mkdir()
    (destination / "reporter/main.go").write_text(reporter)
    docker = f'''FROM --platform=linux/arm64 {BASE} AS build
WORKDIR /work
RUN echo '{GO_SHA}  /usr/local/go/bin/go' | sha256sum --check \\
    && echo '{digest}  /usr/local/go/src/{source_path}' | sha256sum --check
COPY go.mod ./
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg={subject + (',image/png' if name == 'generic' else '')} -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter
FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
'''
    (destination / "Dockerfile").write_text(docker)
    lock = {"runtime": RUNTIME, "base_image": BASE, "source_sha256": digest}
    (destination / "runtime-lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    control = ROOT / entry["control"]
    manifest = {"schema_version": 1, "kind": "standard", "format": fmt, "ecosystem": "go",
                "package": entry["api"], "release": "1.27.1", "api": entry["api"],
                "runtime": RUNTIME, "standard_inventory": str(inventory_path.relative_to(ROOT)),
                "runtime_lock": "runtime-lock.json", "source_sha256": digest,
                "fuzz_engine": "Go native fuzzing", "fuzz_engine_release": "1.27.1",
                "fuzz_engine_sha256": GO_SHA,
                "fuzz_smoke_entrypoint": "/work/harness.test",
                "fuzz_smoke_args": ["-test.list=Fuzz"], "fuzz_smoke_expect": "FuzzParser",
                "toolchain_entrypoint": "/work/reporter", "toolchain_args": ["--toolchain"],
                "base_image": BASE, "platform": "linux/arm64",
                "control": entry["control"], "control_sha256": sha256(control.read_bytes()).hexdigest(),
                "expected_output": EXPECTED[name], "harness": "harness_test.go",
                "fuzz_entry": "FuzzParser", "coverage": f"Go coverpkg instrumentation of standard {subject}",
                "coverage_subject_prefix": subject + "/"}
    if name == "generic":
        manifest["underlying_coverage_subject_prefix"] = "image/png/"
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    for item in SOURCE:
        print(stage(item).relative_to(ROOT))
