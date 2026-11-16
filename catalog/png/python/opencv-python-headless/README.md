# opencv-python-headless — PNG / Python

- **Pinned release:** `5.0.0.93`
- **License:** Apache-2.0
- **Parsed scope:** pixels
- **Underlying family:** OpenCV imgcodecs
- **Local input API:** `cv2.imread(local path, IMREAD_UNCHANGED)`
- **Documentation:** [API reference](<https://docs.opencv.org/5.0/main_modules/imgcodecs.html>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
