# github.com/anthonynsimon/bild/imgio — PNG / Go

- **Pinned release:** `v0.17.1`
- **Upstream:** [source repository](<https://github.com/anthonynsimon/bild>) · [pkg.go.dev](<https://pkg.go.dev/github.com/anthonynsimon/bild/imgio>)
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Go image/png wrapper
- **Local input API:** `Open(path)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/anthonynsimon/bild/imgio@v0.17.1>)
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

[Docker harness and verification receipt](../../../../projects/png/go/github_com_anthonynsimon_bild_imgio/README.md)

```sh
python3 parsarium.py build png go github_com_anthonynsimon_bild_imgio
python3 parsarium.py run png go github_com_anthonynsimon_bild_imgio controls/png/red-green.png
```
