# github.com/disintegration/imaging — PNG / Go

- **Pinned release:** `v1.6.2`
- **Upstream:** [source repository](<https://github.com/disintegration/imaging>) · [pkg.go.dev](<https://pkg.go.dev/github.com/disintegration/imaging>)
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Go image/png wrapper
- **Local input API:** `Open(path)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/disintegration/imaging@v1.6.2>)
- **Catalog evidence:** [parser record](../../../../data/go/png/parsers.json) · [control verification](../../../../data/go/png/verification.json) · [within-ecosystem ranking](../../../../data/go/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "height": 1,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ],
  "width": 2
}
```

Shared underlying parser lineage or wrapper; package count is not an independent engine count.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/go/imaging/README.md)

```sh
python3 parsarium.py build png go imaging
python3 parsarium.py run png go imaging controls/png/red-green.png
```
