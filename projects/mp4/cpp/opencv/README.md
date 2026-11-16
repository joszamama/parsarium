# opencv — MP4 / C++

Pinned release: `5.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/opencv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp opencv
python3 parsarium.py run mp4 cpp opencv controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp opencv CORPUS_DIR runs/mp4-opencv-replay
python3 parsarium.py afl build mp4 cpp opencv
python3 parsarium.py afl prepare mp4 cpp opencv runs/mp4-opencv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
