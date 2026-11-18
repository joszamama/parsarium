# imagesize — ASCII PNM / Python

- **Pinned release:** `2.0.1`
- **Upstream:** [source repository](<https://github.com/shibukawa/imagesize_py>) · [PyPI](<https://pypi.org/project/imagesize/>)
- **License:** MIT
- **Parsed scope:** P3 dimensions only
- **Underlying family:** imagesize PNM header
- **Local input API:** `imagesize.get(local path)`
- **Documentation:** [API reference](<https://github.com/shibukawa/imagesize_py>)
- **Catalog evidence:** [parser record](../../../../data/python/ascii_pnm/parsers.json) · [control verification](../../../../data/python/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/python/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/imagesize/README.md)

```sh
python3 parsarium.py build ascii_pnm python imagesize
python3 parsarium.py run ascii_pnm python imagesize controls/ascii_pnm/red-green.ppm
```
