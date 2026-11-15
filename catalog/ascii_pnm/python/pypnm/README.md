# PyPNM — ASCII PNM / Python

- **Pinned release:** `3.34.24.34`
- **License:** Unlicense
- **Parsed scope:** P3 pixels
- **Underlying family:** PyPNM
- **Local input API:** `pypnm.pnm2list(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/PyPNM/3.34.24.34/>)
- **Catalog evidence:** [parser record](../../../../data/python/ascii_pnm/parsers.json) · [control verification](../../../../data/python/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/python/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
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
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/pypnm/README.md)

```sh
python3 parsarium.py build ascii_pnm python pypnm
python3 parsarium.py run ascii_pnm python pypnm controls/ascii_pnm/red-green.ppm
```
