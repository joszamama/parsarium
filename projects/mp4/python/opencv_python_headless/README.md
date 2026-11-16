# opencv-python-headless — MP4 / Python

Pinned release: `5.0.0.93`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/python/opencv-python-headless/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 python opencv_python_headless
python3 parsarium.py run mp4 python opencv_python_headless controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 python opencv_python_headless CORPUS_DIR runs/mp4-opencv_python_headless-replay
python3 parsarium.py afl build mp4 python opencv_python_headless
python3 parsarium.py afl prepare mp4 python opencv_python_headless runs/mp4-opencv_python_headless-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
