# github.com/perelin/govips/pkg/vips — ASCII PNM / Go

- **Pinned release:** `v0.0.0-20200811153805-fbe430bb7feb`
- **License:** MIT
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** libvips ppmload
- **Local input API:** `Startup(nil); Ppmload(local path); Pngsave(parsed image, temp path)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/perelin/govips/pkg/vips@v0.0.0-20200811153805-fbe430bb7feb>)
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

Shared code lineage or native parser; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_perelin_govips_pkg_vips/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_perelin_govips_pkg_vips
python3 parsarium.py run ascii_pnm go github_com_perelin_govips_pkg_vips controls/ascii_pnm/red-green.ppm
```
