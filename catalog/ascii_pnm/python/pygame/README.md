# pygame — ASCII PNM / Python

- **Pinned release:** `2.6.1`
- **Upstream:** [source repository](<https://github.com/pygame/pygame>) · [PyPI](<https://pypi.org/project/pygame/>)
- **License:** LGPL
- **Parsed scope:** P3 pixels
- **Underlying family:** pygame image PNM loader
- **Local input API:** `pygame.image.load(local path); get_at()`
- **Documentation:** [API reference](<https://www.pygame.org/docs/ref/image.html>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/pygame/README.md)

```sh
python3 parsarium.py build ascii_pnm python pygame
python3 parsarium.py run ascii_pnm python pygame controls/ascii_pnm/red-green.ppm
```
