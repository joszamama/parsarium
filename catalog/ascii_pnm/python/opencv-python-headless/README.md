# opencv-python-headless — ASCII PNM / Python

- **Pinned release:** `5.0.0.93`
- **License:** Apache-2.0
- **Parsed scope:** P3 pixels
- **Underlying family:** OpenCV imgcodecs PXM
- **Local input API:** `cv2.imread(local path, IMREAD_UNCHANGED)`
- **Documentation:** [API reference](<https://docs.opencv.org/5.0/main_modules/imgcodecs.html>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
