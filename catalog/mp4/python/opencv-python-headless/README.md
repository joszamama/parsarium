# opencv-python-headless — MP4 / Python

- **Pinned release:** `5.0.0.93`
- **License:** Apache-2.0
- **Parsed scope:** decoded video frame
- **Underlying family:** OpenCV FFmpeg video backend
- **Local input API:** `cv2.VideoCapture(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/opencv-python-headless/5.0.0.93/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "red_frame": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/opencv_python_headless/README.md)

```sh
python3 parsarium.py build mp4 python opencv_python_headless
python3 parsarium.py run mp4 python opencv_python_headless controls/mp4/red-av.mp4
```
