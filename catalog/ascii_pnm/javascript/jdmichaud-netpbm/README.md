# @jdmichaud/netpbm — ASCII PNM / JavaScript

- **Pinned release:** `0.2.1`
- **License:** MIT
- **Parsed scope:** P3 RGBA pixels and dimensions
- **Underlying family:** jdmichaud Netpbm decoder
- **Local input API:** `decode(localUint8Array)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@jdmichaud/netpbm>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
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
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/javascript/jdmichaud_netpbm/README.md)

```sh
python3 parsarium.py build ascii_pnm javascript jdmichaud_netpbm
python3 parsarium.py run ascii_pnm javascript jdmichaud_netpbm controls/ascii_pnm/red-green.ppm
```
