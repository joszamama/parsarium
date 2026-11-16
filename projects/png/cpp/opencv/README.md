# opencv — PNG / C++

Pinned release: `5.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/opencv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp opencv
python3 parsarium.py run png cpp opencv controls/png/red-green.png
python3 parsarium.py replay png cpp opencv CORPUS_DIR runs/png-opencv-replay
python3 parsarium.py afl build png cpp opencv
python3 parsarium.py afl prepare png cpp opencv runs/png-opencv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
