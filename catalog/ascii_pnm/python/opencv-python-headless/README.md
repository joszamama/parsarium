# opencv-python-headless — ASCII PNM / Python

- **Pinned release:** `5.0.0.93`
- **Upstream:** [source repository](<https://github.com/opencv/opencv-python>) · [PyPI](<https://pypi.org/project/opencv-python-headless/>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/opencv_python_headless/README.md)

```sh
python3 parsarium.py build ascii_pnm python opencv_python_headless
python3 parsarium.py run ascii_pnm python opencv_python_headless controls/ascii_pnm/red-green.ppm
```
