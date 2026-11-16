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

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/opencv_python_headless/README.md)

```sh
python3 parsarium.py build png python opencv_python_headless
python3 parsarium.py run png python opencv_python_headless controls/png/red-green.png
```
