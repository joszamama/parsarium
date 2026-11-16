# @imgdrop/pnm — ASCII PNM / JavaScript

- **Pinned release:** `1.0.2`
- **License:** MIT
- **Parsed scope:** P3 RGB pixels and dimensions
- **Underlying family:** imgdrop PNM decoder
- **Local input API:** `new PNMDecoder(localByteReader).decode()`
- **Documentation:** [API reference](<https://unpkg.com/@imgdrop/pnm@1.0.2/bin/index.d.ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "tuple": "RGB",
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/javascript/imgdrop_pnm/README.md)

```sh
python3 parsarium.py build ascii_pnm javascript imgdrop_pnm
python3 parsarium.py run ascii_pnm javascript imgdrop_pnm controls/ascii_pnm/red-green.ppm
```
