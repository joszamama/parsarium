# rasterio — PNG / Python

- **Pinned release:** `1.5.2`
- **Upstream:** [source repository](<https://github.com/rasterio/rasterio>) · [PyPI](<https://pypi.org/project/rasterio/>)
- **License:** BSD-3-Clause
- **Parsed scope:** pixels
- **Underlying family:** GDAL PNG
- **Local input API:** `rasterio.open(local path).read()`
- **Documentation:** [API reference](<https://rasterio.readthedocs.io/en/stable/quickstart.html>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba0": [
    255,
    0,
    0,
    255
  ],
  "rgba1": [
    0,
    255,
    0,
    255
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/rasterio/README.md)

```sh
python3 parsarium.py build png python rasterio
python3 parsarium.py run png python rasterio controls/png/red-green.png
```
