# opencv-python-headless — ASCII PNM / Python

Pinned release: `5.0.0.93`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/opencv-python-headless/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python opencv_python_headless
python3 parsarium.py run ascii_pnm python opencv_python_headless controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python opencv_python_headless CORPUS_DIR runs/ascii_pnm-opencv_python_headless-replay
python3 parsarium.py afl build ascii_pnm python opencv_python_headless
python3 parsarium.py afl prepare ascii_pnm python opencv_python_headless runs/ascii_pnm-opencv_python_headless-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
