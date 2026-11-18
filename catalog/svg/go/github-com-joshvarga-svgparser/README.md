# github.com/JoshVarga/svgparser — SVG / Go

- **Pinned release:** `v0.0.0-20200804023048-5eaba627a7d1`
- **Upstream:** [source repository](<https://github.com/JoshVarga/svgparser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/JoshVarga/svgparser>)
- **License:** MIT
- **Parsed scope:** rects, root
- **Underlying family:** JoshVarga SVG tree parser
- **Local input API:** `Parse(io.Reader, true).FindAll(rect)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/JoshVarga/svgparser@v0.0.0-20200804023048-5eaba627a7d1>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rects": 2,
  "root": "svg"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_joshvarga_svgparser/README.md)

```sh
python3 parsarium.py build svg go github_com_joshvarga_svgparser
python3 parsarium.py run svg go github_com_joshvarga_svgparser controls/svg/red-green.svg
```
