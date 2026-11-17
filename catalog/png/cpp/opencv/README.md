# opencv — PNG / C++

- **Pinned release:** `5.1.0`
- **License:** Apache-2.0
- **Parsed scope:** RGBA pixels
- **Underlying family:** OpenCV imgcodecs PNG loader over linked libpng
- **Local input API:** `cv::imread(local PNG filename, cv::IMREAD_UNCHANGED) returns cv::Mat with decoded BGRA pixels`
- **Documentation:** [API reference](<https://docs.opencv.org/5.0/main_modules/imgcodecs.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/png/parsers.json) · [control verification](../../../../data/cpp/png/verification.json) · [within-ecosystem ranking](../../../../data/cpp/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

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

The pinned OpenCV imgcodecs dylib links Homebrew libpng 1.6.59. This is a distinct, widely used C++ local-file API sharing libpng as its PNG syntax engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/cpp/opencv/README.md)

```sh
python3 parsarium.py build png cpp opencv
python3 parsarium.py run png cpp opencv controls/png/red-green.png
```
