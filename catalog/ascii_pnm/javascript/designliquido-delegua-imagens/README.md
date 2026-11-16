# @designliquido/delegua-imagens — ASCII PNM / JavaScript

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** P3 RGB pixels and dimensions
- **Underlying family:** Delégua Imagens PPM reader
- **Local input API:** `abrirPPM({}, localPath)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@designliquido/delegua-imagens>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb": [
    255,
    0,
    0,
    0,
    255,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/javascript/designliquido_delegua_imagens/README.md)

```sh
python3 parsarium.py build ascii_pnm javascript designliquido_delegua_imagens
python3 parsarium.py run ascii_pnm javascript designliquido_delegua_imagens controls/ascii_pnm/red-green.ppm
```
