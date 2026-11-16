# napari-netpbmfile — ASCII PNM / Python

- **Pinned release:** `0.0.3`
- **License:** BSD-3-Clause
- **Parsed scope:** P3 pixels
- **Underlying family:** napari-netpbmfile via netpbmfile
- **Local input API:** `napari_netpbmfile.napari_get_reader(local path)(local path)`
- **Documentation:** [API reference](<https://napari.org/dev/plugins/advanced_topics/npe2_migration_guide.html>)
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

The wheel's source exposes napari_get_reader, which delegates to netpbmfile.imread; package metadata omits napari-plugin-engine, pinned separately in requirements.in.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/napari_netpbmfile/README.md)

```sh
python3 parsarium.py build ascii_pnm python napari_netpbmfile
python3 parsarium.py run ascii_pnm python napari_netpbmfile controls/ascii_pnm/red-green.ppm
```
