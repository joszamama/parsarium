# github.com/rustyoz/svg — SVG / Go

- **Pinned release:** `v0.0.0-20260625015314-1aeec84fa7e2`
- **Upstream:** [source repository](<https://github.com/rustyoz/svg>) · [pkg.go.dev](<https://pkg.go.dev/github.com/rustyoz/svg>)
- **License:** MIT
- **Parsed scope:** height, width
- **Underlying family:** rustyoz SVG parser
- **Local input API:** `ParseSvgFromReader(io.Reader, name, scale)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/rustyoz/svg@v0.0.0-20260625015314-1aeec84fa7e2>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "height": "1",
  "width": "2"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_rustyoz_svg/README.md)

```sh
python3 parsarium.py build svg go github_com_rustyoz_svg
python3 parsarium.py run svg go github_com_rustyoz_svg controls/svg/red-green.svg
```
