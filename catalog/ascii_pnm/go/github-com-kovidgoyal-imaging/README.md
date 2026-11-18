# github.com/kovidgoyal/imaging — ASCII PNM / Go

- **Pinned release:** `v1.9.0`
- **Upstream:** [source repository](<https://github.com/kovidgoyal/imaging>) · [pkg.go.dev](<https://pkg.go.dev/github.com/kovidgoyal/imaging>)
- **License:** MIT
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** kovidgoyal Netpbm (imaging.Decode wrapper over imaging/netpbm)
- **Local input API:** `Decode(io.Reader, Backends(GO_IMAGE))`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/kovidgoyal/imaging@v1.9.0>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "height": 1,
  "rgb0": [
    255,
    0,
    0
  ],
  "rgb1": [
    0,
    255,
    0
  ],
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_kovidgoyal_imaging/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_kovidgoyal_imaging
python3 parsarium.py run ascii_pnm go github_com_kovidgoyal_imaging controls/ascii_pnm/red-green.ppm
```
