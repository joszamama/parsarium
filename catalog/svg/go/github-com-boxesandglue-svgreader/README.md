# github.com/boxesandglue/svgreader — SVG / Go

- **Pinned release:** `v0.0.9`
- **Upstream:** [source repository](<https://github.com/boxesandglue/svgreader>) · [pkg.go.dev](<https://pkg.go.dev/github.com/boxesandglue/svgreader>)
- **License:** BSD-3-Clause
- **Parsed scope:** elements
- **Underlying family:** boxesandglue SVG reader
- **Local input API:** `Parse(io.Reader).Elements`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/boxesandglue/svgreader@v0.0.9>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "elements": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_boxesandglue_svgreader/README.md)

```sh
python3 parsarium.py build svg go github_com_boxesandglue_svgreader
python3 parsarium.py run svg go github_com_boxesandglue_svgreader controls/svg/red-green.svg
```
