# openpnp-opencv — ASCII PNM / Java

- **Pinned release:** `4.9.0-0`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** OpenPnP Java binding over native OpenCV PNM decoder
- **Local input API:** `OpenCV.loadLocally(); Imgcodecs.imread(String local path)`
- **Documentation:** [API reference](<https://docs.opencv.org/4.9.0/d4/da8/group__imgcodecs.html>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
