# devil — ASCII PNM / C

- **Pinned release:** `1.8.0`
- **License:** LGPL-2.1-only
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** DevIL PNM reader
- **Local input API:** `ilLoadImage(const ILstring path); ilGetInteger(IL_IMAGE_WIDTH/HEIGHT); ilGetData()`
- **Documentation:** [API reference](<https://openil.sourceforge.net/docs/DevIL%20Reference%20Guide.pdf>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0,
    255
  ],
  "second": [
    0,
    255,
    0,
    255
  ]
}
```

DevIL ilLoadImage parsed P3; primary SourceForge project lacks a comparable GitHub star metric.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/c/devil/README.md)

```sh
python3 parsarium.py build ascii_pnm c devil
python3 parsarium.py run ascii_pnm c devil controls/ascii_pnm/red-green.ppm
```
