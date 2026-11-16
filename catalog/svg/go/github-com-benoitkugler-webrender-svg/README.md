# github.com/benoitkugler/webrender/svg — SVG / Go

- **Pinned release:** `v0.0.15`
- **License:** BSD-3-Clause
- **Parsed scope:** height, width
- **Underlying family:** webrender SVG parser
- **Local input API:** `Parse(io.Reader, baseURL, imageLoader, urlFetcher).DisplayedSize()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/benoitkugler/webrender/svg@v0.0.15>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "height": 1,
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_benoitkugler_webrender_svg/README.md)

```sh
python3 parsarium.py build svg go github_com_benoitkugler_webrender_svg
python3 parsarium.py run svg go github_com_benoitkugler_webrender_svg controls/svg/red-green.svg
```
