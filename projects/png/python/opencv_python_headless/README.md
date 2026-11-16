# opencv-python-headless — PNG / Python

Pinned release: `5.0.0.93`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/opencv-python-headless/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python opencv_python_headless
python3 parsarium.py run png python opencv_python_headless controls/png/red-green.png
python3 parsarium.py replay png python opencv_python_headless CORPUS_DIR runs/png-opencv_python_headless-replay
python3 parsarium.py afl build png python opencv_python_headless
python3 parsarium.py afl prepare png python opencv_python_headless runs/png-opencv_python_headless-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
