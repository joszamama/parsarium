# cogentcore.org/core/svg — SVG / Go

- **Pinned release:** `v0.5.30`
- **License:** BSD-3-Clause
- **Parsed scope:** parsed viewBox and two rectangle elements
- **Underlying family:** Goki/Cogent SVG lineage
- **Local input API:** `NewSVG(size).ReadXML(io.Reader).Root.ViewBox`
- **Documentation:** [API reference](<https://pkg.go.dev/cogentcore.org/core/svg@v0.5.30>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "height": 1,
  "width": 2,
  "elements": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/cogentcore_org_core_svg/README.md)

```sh
python3 parsarium.py build svg go cogentcore_org_core_svg
python3 parsarium.py run svg go cogentcore_org_core_svg controls/svg/red-green.svg
```
