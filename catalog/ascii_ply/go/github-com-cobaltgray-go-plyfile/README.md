# github.com/cobaltgray/go-plyfile — ASCII PLY / Go

- **Pinned release:** `v0.0.0-20210513130740-b21b0efca069`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY vertex count and coordinate
- **Underlying family:** Greg Turk plyfile C family
- **Local input API:** `PlyOpenForReading(string); PlyGetElement(CPlyFile, interface{}, uintptr)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/cobaltgray/go-plyfile@v0.0.0-20210513130740-b21b0efca069>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "last": {
    "X": 0,
    "Y": 1,
    "Z": 0
  }
}
```

Go wrapper fork over the same Greg Turk C PLY parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_cobaltgray_go_plyfile/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_cobaltgray_go_plyfile
python3 parsarium.py run ascii_ply go github_com_cobaltgray_go_plyfile controls/ascii_ply/triangle.ply
```
